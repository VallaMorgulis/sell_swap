from config.celery import app


from news.management.commands.parse_news import main


@app.task
def parsing():
    main()
    # url = get_html('https://www.sport-express.ru/news/')
    # soup = get_soup(url)
    # links = get_list_links(soup)
    # with Pool(40) as pool:
    #     pool.map(make_all, links)
