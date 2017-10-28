from fetch_data import get_post_emojis

postcode = 'BRjXi58h8pV'

res = get_post_emojis(postcode, limit_comments=50, nr_most_common=3)
print(res)