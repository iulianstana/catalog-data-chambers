# catalog-data-chambers

This is a Python 3 + Scrapy crawling / web scraping application. Momentarily, there is only one spider (accordingly named *CameraDeputatilorInitiatives*) which crawls the website [wwww.cdep.ro](http://www.cdep.ro) and gathers data about the legal initiatives of all the deputies whose profiles are available on the website.

## Requirements

The only requirements for running the application are *Python 3.6.1* and *Scrapy 1.3.3*. For development, unless one wants to generate test cases by snapshotting the website, the same requirements apply. In the case where generating tests is desired, *Selenium* with *PhantomJS* is required.

If you use _pip_, we put in a *requirements.txt* and a *requirements_dev.txt* file for you.

## Instructions

We recommend you use *pip* and *virtualenv* to setup your environment.

- macOS (tested on 10.12)
  1. Install [homebrew](https://brew.sh).
  2. `brew install python3`
  3. `pip3 install virtualenv`
- Ubuntu (tested on 16.04 LTS)
  1. `pip3 install virtualenv`

The following should be common on both:
1. `git clone https://github.com/code4romania/catalog-data-chambers`
2. `cd catalog-data-chambers`
3. `virtualenv -p python3 cdc_env`
4. `source cdc_env/bin/activate`
5. `pip install -r requirements.txt`
7. `scrapy crawl CameraDeputatilorInitiatives -a year=2016 -o 2016.json`

These instructions are tested and work in the systems specified, but they do not have to be exacuted as given. You can customize your setup to suit your needs.

## Commands

### Spider commands (*CameraDeputatilorInitiatives*)

#### year

An election cycle lasts 4 year and is named by the year in which it started. For example, we name the 2008–2016 cycle *the 2008 cycle*. You can use this command to crawl a specific cycle.

###### Example

Say you only want to crawl the 2000 cycle (this means initiatives between 2000 and 2004). For this you can use `scrapy crawl CameraDeputatilorInitiatives -a year=2000`.

#### years

The same as year, but you can have multiple cycles.

###### Example

Say you want to crawl the initiatives between 2004 and 2012. This period is made up of two cycles: 2004 and 2008. To accomplish this you can use `scrapy crawl CameraDeputatilorInitiatives -a years='2004 2008'`.

#### after

You can use _after_ to crawl only cycles that began in or after a given year.

###### Example

Say you want to crawl all the initiatives from 2012 to present, to accomplish this you can use `scrapy crawl CameraDeputatilorInitiatives -a after=2012`.

### Testing commands

If you want to make sure the spider still yields the same values and request on our set of input data, you can run `scrapy test`.

### Generating tests

Sometimes you find edge cases like weird characters, unexpected elements, and so on. After you fix the problem, you want to ensure that in the future the spider does not fail on these edge cases again. For this we developed an automatic test generation tool. You can generate a test by running `scrapy gentest <url> <spider> <method>`. The URL tells the generator what page to save a local HTML snapshot and spider results of. The other arguments specify the spider and the method of the spider which should parse the response and be used to generate the test answer. Frozen tests responses and results are saved in [the frozen directory](test/responses/frozen). When you generate a test, the generator also saves a .png screenshot of the website, so you can reference it later should the need arise.

 **Right now there is no proper method to manage these tests, but we are working on it.** However, you can update a test by regenerating with the same URL, spider, and method. You can also delete it directly from [the frozen directory](test/responses/frozen).
