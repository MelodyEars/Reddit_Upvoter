from interface import user_deasire_data

'https://www.reddit.com/r/drawing/comments/101dlrm/this_got_removed_for_being_nsfw_so_here_is_day/'
'Looks amazing!!!'
'https://www.reddit.com/r/ffxiv/comments/10hf1e1/nsfw/'
"This is Geralt, but what is the name of the elf? Are there ero-content with her?"
'https://www.reddit.com/r/PornMemes/comments/10exyyz/eat_fresh/'
"It's so deep!"
def main():
    # interface
    link_reddit, approves_int, comments_int = user_deasire_data()
    # 4 approves - comment = count for for 2
    remaining_approvals = approves_int - comments_int

    # db
    # 4 reset all data in the worked_is

    ### for 3 list random comment
    # get from db account not worked random choice
    # approves and comment on the Reddit
    # db rewrite 1 is worked profile

    ### for 2 range count for for 2
    # get from db account not worked random choice
    # approves
    # db rewrite 1 is worked profile

    # TODO handling error BAN

if __name__ == '__main__':
    main()
