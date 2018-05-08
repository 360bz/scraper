import scraperwiki
import urlparse
import lxml.html

# create a new function, which gets passed a variable we're going to call 'url'
def scrape_imdb(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    #line below selects all <div class="reveal-modal medium"> - note that because there is a space in the value of the div class, we need to use a space to indicate that
    rows = root.cssselect("div.lister-item-content")
    for row in rows:
        print row
        # Set up our data record - we'll need it later
        record = {}
        a = row.cssselect("a") #grab all <a> tags within our <div>
        title = a[0].text
        #repeat process for <span class="lister-item-year text-muted unbold"> 
        item_year = row.cssselect("span.lister-item-year.text-muted.unbold")
        year = item_year[0].text
        #repeat process for <span class="value">
        value = row.cssselect("span.value")
        imdb_rating = value[0].text
        #repeat for <span class="metascore  favorable">
        meta = row.cssselect("span.metascore.favorable")
        metascore = meta[0].text
        #repeat for <span class="genre">
        gen = row.cssselect("span.genre")
        genre = gen[0].text
        #repeat process for <p class="text-muted">
        txt = row.cssselect("p.text-muted")
        description = txt[1].text_content()
        href = row.cssselect("a")
        director = href[12].text
        #record['URL'] = url
        record['Title'] = title
        record['Year'] = year
        record['IMDB Rating'] = imdb_rating
        record['Metascore'] = metascore
        record['Genre'] = genre
        record['Description'] = description
        record['Director'] = director
        print record, '------------'
        # Finally, save the record to the datastore - 'Name' is our unique key
        scraperwiki.sqlite.save(["Title"], record)
        
imdblist = ['pro.imdb.com/inproduction/development?ref_=hm_nv_tt_dev#type=movie&status=DEVELOPMENT%2CPRE_PRODUCTION%2CPRODUCTION%2CPOST_PRODUCTION&year=2020-2020&country=US%2CGB%2CCA%2CAU&sort=ranking&pos=0']
for url in imdblist:
    fullurl = 'https://'+url
    print 'scraping ', fullurl
    scrape_imdb(fullurl)
