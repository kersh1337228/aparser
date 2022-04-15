# Asynchronous parallel parser
    Description:
This parser can be used to fast parse big amount of data.
You can use it in your applications if you need to get stock
market data or online market data for example.

>All the code is located in 'main.py' file, so every step that is
listed below (in Usage guide section) should have been made in this file.

    Usage guide:
1) Put your request url into ***url*** global constant
2) Put your necessary request headers into ***headers*** global constant
3) Set up error handling in the ***parse()*** function.
Below the *'# Bad request error handling here'* comment.
4) Set up pagination handling in ***session.get()*** method in the ***parse_coroutine()*** function.
5) Set up parsing below the *'# Handling parsed data here'* comment.
6) Set up parsing results handling in the ***parse_result_handle()*** function.