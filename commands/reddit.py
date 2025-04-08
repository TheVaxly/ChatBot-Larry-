import discord
import requests
import random

async def reddit(ctx, subreddit, *args):
    try:
        sort_method = "hot"
        media_type = "all"
        time_period = "day"

        valid_sorts = ["hot", "new", "top", "rising", "best"]
        valid_media_types = ["image", "video", "gallery"]
        valid_time_periods = ["hour", "day", "week", "month", "year", "all"]

        if len(args) == 1:
            arg = args[0].lower()
            if arg in valid_sorts:
                sort_method = arg
            elif arg in valid_media_types:
                media_type = arg
            elif arg in valid_time_periods:
                time_period = arg
            else:
                await ctx.send(embed=discord.Embed(
                    title="Error",
                    description="Invalid argument.",
                    color=discord.Color.red()))
                return
        elif len(args) == 2:
            arg1, arg2 = args[0].lower(), args[1].lower()
            if arg1 in valid_sorts:
                sort_method = arg1
                if arg2 in valid_media_types:
                    media_type = arg2
                elif arg2 in valid_time_periods:
                    time_period = arg2
                else:
                    await ctx.send(embed=discord.Embed(
                        title="Error",
                        description="Second argument must be valid media or time period.",
                        color=discord.Color.red()))
                    return
            else:
                await ctx.send(embed=discord.Embed(
                    title="Error",
                    description="First argument must be a valid sort method.",
                    color=discord.Color.red()))
                return
        elif len(args) == 3:
            sort_arg, time_arg, media_arg = map(str.lower, args)
            if sort_arg not in valid_sorts or time_arg not in valid_time_periods or media_arg not in valid_media_types:
                await ctx.send(embed=discord.Embed(
                    title="Error",
                    description="Invalid combination of arguments.",
                    color=discord.Color.red()))
                return
            sort_method = sort_arg
            time_period = time_arg
            media_type = media_arg
        elif len(args) > 3:
            await ctx.send(embed=discord.Embed(
                title="Error",
                description="Too many arguments.",
                color=discord.Color.red()))
            return

        base_url = f"https://www.reddit.com/r/{subreddit}"
        if sort_method == "top":
            url = f"{base_url}/top.json?t={time_period}&limit=100"
        else:
            url = f"{base_url}/{sort_method}.json?limit=100"

        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json'
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            await ctx.send(embed=discord.Embed(
                title="Error",
                description=f"Couldn't access r/{subreddit}.",
                color=discord.Color.red()))
            return

        data = response.json()
        posts = []

        for post in data['data']['children']:
            post_data = post['data']
            if 'post_hint' in post_data:
                post_type = post_data['post_hint']
            else:
                post_type = "gallery" if 'is_gallery' in post_data and post_data['is_gallery'] else None

            if media_type == "all":
                posts.append(post_data)
            elif media_type == "image" and post_type == "image":
                posts.append(post_data)
            elif media_type == "video" and post_type == "video":
                posts.append(post_data)
            elif media_type == "gallery" and post_type == "gallery":
                posts.append(post_data)

        if not posts:
            await ctx.send(embed=discord.Embed(
                title="Error",
                description=f"No {media_type} posts found.",
                color=discord.Color.red()))
            return

        post = random.choice(posts)
        time_info = f" | Time: {time_period.capitalize()}" if sort_method == "top" else ""

        # Function to fetch a random comment and one of its replies
        def fetch_random_comment_with_reply(post):
            comments_url = f"https://www.reddit.com{post['permalink']}.json"
            comments_response = requests.get(comments_url, headers=headers)
            if comments_response.status_code == 200:
                comments_data = comments_response.json()
                if len(comments_data) > 1:
                    comments = comments_data[1]['data']['children']
                    comments = [c['data'] for c in comments if c['kind'] == 't1' and not c['data'].get('stickied', False)]
                    if comments:
                        comment = random.choice(comments)
                        # Fetch replies for the selected comment
                        if 'replies' in comment and comment['replies'] and comment['replies']['data']['children']:
                            reply = random.choice(comment['replies']['data']['children'])
                            return comment, reply['data']
                        return comment, None
            return None, None

        # === GALLERY HANDLER ===
        if 'is_gallery' in post and post['is_gallery']:
            media = post['media_metadata']
            image_ids = list(media.keys())
            image_urls = [
                media[iid]['p'][-1]['u'].replace("&amp;", "&") for iid in image_ids
            ]
            current_index = 0

            def build_embed(index, comment=None, reply=None):
                embed = discord.Embed(
                    title=post['title'][:256],
                    url=f"https://reddit.com{post['permalink']}",
                    color=discord.Color.orange(),
                    description=f"📷 Gallery post - Image {index + 1}/{len(image_urls)}"
                )
                embed.set_image(url=image_urls[index])
                footer_text = f"👍 {post['ups']:,} | 💬 {post['num_comments']:,} | u/{post['author']} | r/{subreddit} | Sort: {sort_method.capitalize()}{time_info} | Type: Gallery"
                embed.set_footer(text=footer_text)

                if comment:
                    comment_id = comment['id']
                    comment_author = comment.get('author', '[deleted]')
                    comment_body = comment.get('body', '[No content]')
                    embed.add_field(name="💬 Random Comment", value=f"```t1_{comment_id}-post-rtjson-content\n{comment_body}```", inline=False)

                    if reply:
                        reply_author = reply.get('author', '[deleted]')
                        reply_body = reply.get('body', '[No content]')
                        embed.add_field(name="🔁 Reply", value=f"```t1_{reply['id']}-post-rtjson-content\n{reply_body}```", inline=False)

                return embed

            # Fetch a random comment and one of its replies
            comment, reply = fetch_random_comment_with_reply(post)

            message = await ctx.send(embed=build_embed(current_index, comment, reply))
            await message.add_reaction("⬅️")  # For gallery navigation
            await message.add_reaction("➡️")  # For gallery navigation
            await message.add_reaction("⬆️")  # For comment navigation
            await message.add_reaction("⬇️")  # For comment navigation

            # Initialize comment index
            current_comment_index = 0
            comments = []  # List to hold comments

            while True:
                try:
                    reaction, user = await ctx.bot.wait_for("reaction_add", timeout=60.0)
                    if reaction.message.id != message.id:
                        continue  # Ignore reactions on other messages

                    if str(reaction.emoji) == "⬅️":
                        current_index = (current_index - 1) % len(image_urls)
                    elif str(reaction.emoji) == "➡️":
                        current_index = (current_index + 1) % len(image_urls)
                    elif str(reaction.emoji) == "⬆️":
                        # Fetch comments if they are not already fetched
                        if not comments:
                            comments_url = f"https://www.reddit.com{post['permalink']}.json"
                            comments_response = requests.get(comments_url, headers=headers)
                            if comments_response.status_code == 200:
                                comments_data = comments_response.json()
                                comments = comments_data[1]['data']['children']
                                comments = [c['data'] for c in comments if c['kind'] == 't1' and not c['data'].get('stickied', False)]
                        # Navigate through comments
                        if comments:
                            current_comment_index = (current_comment_index + 1) % len(comments)
                            comment, reply = fetch_random_comment_with_reply(post)
                            await message.edit(embed=build_embed(current_index, comments[current_comment_index], reply))

                    elif str(reaction.emoji) == "⬇️":
                        # Fetch comments if they are not already fetched
                        if not comments:
                            comments_url = f"https://www.reddit.com{post['permalink']}.json"
                            comments_response = requests.get(comments_url, headers=headers)
                            if comments_response.status_code == 200:
                                comments_data = comments_response.json()
                                comments = comments_data[1]['data']['children']
                                comments = [c['data'] for c in comments if c['kind'] == 't1' and not c['data'].get('stickied', False)]
                        # Navigate through comments
                        if comments:
                            current_comment_index = (current_comment_index - 1) % len(comments)
                            comment, reply = fetch_random_comment_with_reply(post)
                            await message.edit(embed=build_embed(current_index, comments[current_comment_index], reply))

                    await message.edit(embed=build_embed(current_index, comment, reply))
                    await message.remove_reaction(reaction.emoji, user)
                except Exception as e:
                    break

        # === VIDEO HANDLER ===
        elif 'is_video' in post and post['is_video']:
            embed = discord.Embed(
                title=post['title'][:256],
                url=f"https://reddit.com{post['permalink']}",
                color=discord.Color.orange(),
                description="▶️ Video post"
            )
            if 'preview' in post and 'images' in post['preview']:
                embed.set_image(url=post['preview']['images'][0]['source']['url'])
            embed.set_footer(text=f"👍 {post['ups']:,} | 💬 {post['num_comments']:,} | u/{post['author']} | r/{subreddit} | Sort: {sort_method.capitalize()}{time_info} | Type: Video")

            # Get a comment and add it to the embed
            comment, reply = fetch_random_comment_with_reply(post)
            if comment:
                comment_id = comment['id']
                comment_author = comment.get('author', '[deleted]')
                comment_body = comment.get('body', '[No content]')
                embed.add_field(name="💬 Random Comment", value=f"```t1_{comment_id}-post-rtjson-content\n{comment_body}```", inline=False)

                if reply:
                    reply_author = reply.get('author', '[deleted]')
                    reply_body = reply.get('body', '[No content]')
                    embed.add_field(name="🔁 Reply", value=f"```t1_{reply['id']}-post-rtjson-content\n{reply_body}```", inline=False)

            await ctx.send(embed=embed)

        # === IMAGE HANDLER ===
        else:
            embed = discord.Embed(
                title=post['title'][:256],
                url=f"https://reddit.com{post['permalink']}",
                color=discord.Color.orange()
            )
            if 'url' in post:
                url = post['url']
                if any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                    embed.set_image(url=url)
                elif 'preview' in post and 'images' in post['preview']:
                    embed.set_image(url=post['preview']['images'][0]['source']['url'])

            embed.set_footer(text=f"👍 {post['ups']:,} | 💬 {post['num_comments']:,} | u/{post['author']} | r/{subreddit} | Sort: {sort_method.capitalize()}{time_info} | Type: Image")

            # Get a comment and its reply
            comment, reply = fetch_random_comment_with_reply(post)
            if comment:
                comment_id = comment['id']
                comment_author = comment.get('author', '[deleted]')
                comment_body = comment.get('body', '[No content]')
                embed.add_field(name="💬 Random Comment", value=f"```t1_{comment_id}-post-rtjson-content\n{comment_body}```", inline=False)

                if reply:
                    reply_author = reply.get('author', '[deleted]')
                    reply_body = reply.get('body', '[No content]')
                    embed.add_field(name="🔁 Reply", value=f"```t1_{reply['id']}-post-rtjson-content\n{reply_body}```", inline=False)

            await ctx.send(embed=embed)

    except Exception as e:
        print(f"Error fetching Reddit post: {e}")
        await ctx.send(embed=discord.Embed(
            title="Error",
            description="Something went wrong while fetching the Reddit post.",
            color=discord.Color.red()))
