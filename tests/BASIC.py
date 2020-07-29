from buildaspider import Spider


mySpider = Spider('test_config/basic.ini')

mySpider.weave()

print(mySpider.visited_urls)
print(mySpider.broken_urls)
print('asdasd')
