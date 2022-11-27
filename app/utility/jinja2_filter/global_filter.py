def filter_list(app):

    # jinja global filter
    @app.template_filter()
    def currency_format(value):
        return format(int(value), ',d')
