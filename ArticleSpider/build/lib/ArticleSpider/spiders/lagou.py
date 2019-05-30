# -*- coding: utf-8 -*-
from datetime import datetime
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from items import ArticleItemLoader, LagouJobItem
from ArticleSpider.utils.common import get_md5


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com']

    rules = (
        Rule(LinkExtractor(allow=r'zhaopin/.*'), follow=True),
        Rule(LinkExtractor(allow=r'gongsi/j\d+.html'), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        """解析职位信息"""
        item_loader = ArticleItemLoader(item=LagouJobItem(), response=response)

        item_loader.add_css("title", ".job-name::attr(title)")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("salary", ".job_request .salary::text")
        item_loader.add_css("job_city", ".job_request p span:nth-child(2)::text")
        item_loader.add_css("work_years", ".job_request p span:nth-child(3)::text")
        item_loader.add_css("degree_need", ".job_request p span:nth-child(4)::text")
        item_loader.add_css("job_type", ".job_request p span:nth-child(5)::text")
        item_loader.add_css("publish_time", ".publish_time::text")
        item_loader.add_css("tags", ".position-label li::text")
        item_loader.add_css("job_advantage", ".job-advantage p::text")
        item_loader.add_css("job_desc", ".job-detail")
        item_loader.add_css("job_addr", ".work_addr")
        item_loader.add_css("company_name", "#job_company dt a img::attr(alt)")
        item_loader.add_css("company_url", "#job_company dt a::attr(href)")
        item_loader.add_value("crawl_time", datetime.now())

        job_item = item_loader.load_item()
        return job_item
