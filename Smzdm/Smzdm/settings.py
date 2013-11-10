#coding=utf-8
BOT_NAME = 'Smzdm'

SPIDER_MODULES = ['Smzdm.spiders']
NEWSPIDER_MODULE = 'Smzdm.spiders'

ITEM_PIPELINES=['Smzdm.pipelines.SmzdmPipeline']

#mongodb set
MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'scrapy'
MONGODB_TEMP_COLLECTION = 'smzdm_temp'
MONGODB_COLLECTION = 'smzdm'
MONGODB_UNIQ_KEY = 'id'
MONGODB_ITEM_ID_FIELD = '_id'
MONGODB_SAFE = True

#RETRY_ENABLED = False
DOWNLOAD_TIMEOUT = 60
LOG_FILE='smzdm.log'
LOG_LEVEL='INFO'
#REDIRECT_ENABLED = False

#app seting
START_URL = ['http://www.liuzhuni.com',
             'http://www.smzdm.com',
             #'http://zhi.zhe800.com',
             'http://www.91tehui.com',
             'http://www.tsdxb.com',
             #'http://www.huihui.cn/deals',
             'http://www.tz100.com',
             'http://www.kiees.com/?cat=43',
             'http://pianyiduo.net',
             'http://www.youhuiyouhui.com',
             'http://www.czfxh.com',
             'http://www.msmpy.com',
             'http://www.qugou365.com',
             'http://wabcw.info',
             'http://www.5i5tao.com',
             'http://www.tdpyh.com',
             'http://www.mtyhd.com',
             'http://www.mgpyh.com',
             'http://www.smzdt.com',
             'http://www.360zdm.com']

#START_URL = ['http://www.etao.com']
OUTFILE = 'output_result.json'
CUT_TIME = 3600*24
MAX_ITEM_NUM = 50
URL_TO_NAME = {'http://www.smzdm.com':'SMZDM',
               'http://www.liuzhuni.com' : 'LZN',
               'http://www.zhizhizhi.com' : 'ZZZ',
               'http://zhi.zhe800.com' : 'Z800',
               'http://www.91tehui.com' : '91TH',
               'http://www.tsdxb.com' : 'TSDXB',
               'http://www.huihui.cn/deals' : 'HH',
               'http://www.tz100.com' : 'TZ',
               'http://www.kiees.com/?cat=43' : 'FXZDM',
               'http://pianyiduo.net' : 'PYD',
               'http://www.youhuiyouhui.com' : 'YHYH',
               'http://www.czfxh.com' : 'CZFXH',
               'http://www.dealwithem.com' : 'DWM',
               'http://www.msmpy.com' : 'MSMPY',
               'http://www.qugou365.com' : 'QG',
               'http://wabcw.info' : 'WABCW',
               'http://www.5i5tao.com' : '5TAO',
               'http://www.tdpyh.com' : 'TDPYH',
               'http://www.mtyhd.com' : 'MTYHD',
               'http://www.mgpyh.com' : 'MGPYH',
               #'http://www.smzdt.com' : 'SMZDT',
               'http://www.360zdm.com' : '360ZDM'}
PATH_CONFIG={
'NAME_TO_PRE' : {'SMZDM' : 'http://www.smzdm.com',
                 'LZN' : 'http://www.liuzhuni.com',
                 'ZZZ' : 'http://www.zhizhizhi.com',
                 'Z800' : 'http://zhi.zhe800.com',
                 '91TH' : 'http://www.91tehui.com',
                 'TSDXB' : 'http://www.tsdxb.com',
                 'HH' : 'http://www.huihui.cn',
                 'TZ' : 'http://www.tz100.com',
                 'FXZDM' : 'http://www.kiees.com',
                 'PYD' : 'http://pianyiduo.net',
                 'YHYH' : 'http://www.youhuiyouhui.com',
                 'CZFXH' : 'http://www.czfxh.com',
                 'DWM' : 'http://www.dealwithem.com',
                 'MSMPY' : 'http://www.msmpy.com',
                 'QG' : 'http://www.qugou365.com/',
                 'WABCW' : 'http://wabcw.info',
                 '5TAO' : 'http://www.5i5tao.com',
                 'TDPYH' : 'http://www.tdpyh.com',
                 'MTYHD' : 'http://www.mtyhd.com',
                 'MGPYH' : 'http://www.mgpyh.com',
                 'SMZDT' : 'http://www.smzdt.com',
                 '360ZDM' : 'http://www.360zdm.com'},
'NAME_TO_SHOW' : {'SMZDM':'什么值得买',
                  'LZN' : '留住你',
                  'ZZZ' : '值得买',
                  'Z800' : '折800',
                  '91TH' : '91特惠',
                  'TSDXB' : '天上掉馅饼',
                  'HH' : '惠惠',
                  'TZ' : '淘者',
                  'FXZDM' : '发现值得买',
                  'PYD' : '便宜多',
                  'YHYH' : '优惠优惠网',
                  'CZFXH' : '超值分享会',
                  'DWM' : 'DEALWITHME',
                  'MSMPY' : '买什么便宜',
                  'QG' : '趣购365',
                  'WABCW' : '我爱白菜网',
                  '5TAO' : '我爱我的淘',
                  'TDPYH' : '淘点便宜货',
                  'MTYHD' : '每天优惠多',
                  'MGPYH' : '买个便宜货',
                  'SMZDT' : '什么值得淘',
                  '360ZDM' : '360值得买'},
'MAIN_PATH' : {'SMZDM':'//div[@class="perContentBox"]',
               'LZN' : '//li[@class="con_list "]',
               'ZZZ' : '//div[@class="list_box_l"]',
               'Z800' : '//div[@class="deal"]',
               '91TH' : '//div[@class="list_summary perContentBox"]',
               'TSDXB' : '//div[@class="con_left_cp con_left_cp1"]',
               'HH' : '//li[@class="clearfix "]',
               'TZ' : '//div[@class="cell"]',
               'FXZDM' : '//div[@class="postbox"]',
               'PYD' : '//div[@class="list_summary perContentBox"]',
               'YHYH' : '//div[@class="post clearfix"]',
               'CZFXH' : '//div[@class="post"]',
               'DWM' : '//div[@class="boxes boxesext"]',
               'MSMPY' : '//div[@class="perContentBox list_summary "]',
               'QG' : '//div[@class="title2"]',
               'WABCW' : '//div[@class="post"]',
               '5TAO' : '//div[@id="content"]/article/section',
               'TDPYH' : '//div[@class="con_title"]',
               'MTYHD' : '//div[@class="list_summary perContentBox"]',
               'MGPYH' : '//div[@class="content yui3-u-2-3"]',
               'SMZDT' : '//span[@class="conName"]',
               '360ZDM' : '//h2[@class="post-title"]'},
'TITLE_PATH' : {'SMZDM':['h2[@class="con_title noBg"]/a/@title'],
                'LZN' : ['a/text()'],
                'ZZZ' : ['ul/h2/a/@title'],
                'Z800' : ['h3/span/a/text()'],
                '91TH' : ['div[@class="list_title"]/a/@title','div[@class="list_title"]/a/span/text()'],
                'TSDXB' : ['h2/a/text()','h2/a/span/text()'],
                'HH' : ['h3/a/text()','h4/text()'],
                'TZ' : ['table/tbody/tr/td/h2/a/text()','table/tbody/tr/td/h2/a/span/text()'],
                'FXZDM' : ['div/a/@title'],
                'PYD' : ['div[@class="list_title"]/a/@title'],
                'YHYH' : ['h2[@class="title"]/a/text()'],
                'CZFXH' : ['h2/a/text()'],
                'DWM' : ['h1[@class="headcolor"]/a/text()'],
                'MSMPY' : ['.//span[@class="conName"]/a/text()'],
                'QG' : ['a/text()'],
                'WABCW' : ['h2/a/text()'],
                '5TAO' : ['div[@class="title"]/h2/a/text()'],
                'TDPYH' : ['span[@class="conName"]/a/text()'],
                'MTYHD' : ['div[@class="list_title"]/a/text()'],
                'MGPYH' : ['h1[@class="title"]/a/text()'],
                'SMZDT' : ['a/text()'],
                '360ZDM' : ['a/text()']},
'PUB_TIME_PATH' : {'SMZDM' : 'div[@class="dateTime"]/text()',
                   'LZN' : './/span[@class="pub_time"]/text()',
                   'ZZZ' : 'NONE',
                   'Z800' : 'h3/em/text()',
                   '91TH' : 'div[@class="metas"]/span[@class="date"]/text()',
                   'TSDXB' : 'NONE',
                   'HH' : 'NONE',
                   'TZ' : 'NONE',
                   'FXZDM' : 'NONE',
                   'PYD' : './/span[@class="date"]/text()',
                   'YHYH' : 'NONE',
                   'CZFXH' : 'NONE',
                   'DWM' : 'NONE',
                   'MSMPY' : './/div[@class="conTime"]/text()',
                   'QG' : 'NONE',
                   'WABCW' : 'NONE',
                   '5TAO' : 'NONE',
                   'TDPYH' : 'NONE',
                   'MTYHD' : 'NONE',
                   'MGPYH' : 'NONE',
                   'SMZDT' : 'NONE',
                   '360ZDM' : 'NONE'},
'PUB_TIME_FORMAT' : {'SMZDM' : '%m-%d %H:%M',
                     'LZN' : '%Y-%m-%d %H:%M:%S',
                     'ZZZ' : 'NONE',
                     'Z800' : '%Y/%m/%d %H:%M',
                     '91TH' : '%Y-%m-%d %H:%M',
                     'TSDXB' : 'NONE',
                     'HH' : 'NONE',
                     'TZ' : 'NONE',
                     'FXZDM' : 'NONE',
                     'PYD' : '%Y-%m-%d %H:%M',
                     'YHYH' : 'NONE',
                     'CZFXH' : 'NONE',
                     'DWM' : 'NONE',
                     'MSMPY' : '%m-%d %H:%M',
                     'QG' : 'NONE',
                     'WABCW' : 'NONE',
                     '5TAO' : 'NONE',
                     'TDPYH' : 'NONE',
                     'MTYHD' : 'NONE',
                     'MGPYH' : 'NONE',
                     'SMZDT' : 'NONE',
                     '360ZDM' : 'NONE'},
'CONTENT_URL' : {'SMZDM' : 'h2[@class="con_title noBg"]/a/@href',
                 'LZN' : 'a/@href',
                 'ZZZ' : 'ul/h2/a/@href',
                 'Z800' : 'h3/span/a/@href',
                 '91TH' : 'div[@class="list_title"]/a/@href',
                 'TSDXB' : 'h2/a/@href',
                 'HH' : 'h3/a/@href',
                 'TZ' : 'table/tbody/tr/td/h2/a/@href',
                 'FXZDM' : 'div/a/@href',
                 'PYD' : 'div[@class="list_title"]/a/@href',
                 'YHYH' : 'h2[@class="title"]/a/@href',
                 'CZFXH' : 'h2/a/@href',
                 'DWM' : 'h1[@class="headcolor"]/a/@href',
                 'MSMPY' : './/span[@class="conName"]/a/@href',
                 'QG' : 'a/@href',
                 'WABCW' : 'h2/a/@href',
                 '5TAO' : 'div[@class="title"]/h2/a/@href',
                 'TDPYH' : 'span[@class="conName"]/a/@href',
                 'MTYHD' : 'div[@class="list_title"]/a/@href',
                 'MGPYH' : 'h1[@class="title"]/a/@href',
                 'SMZDT' : 'a/@href',
                 '360ZDM' : 'a/@href'},
'NEXT_PAGE' : {'SMZDM' : '//a[@class="pagedown"]/@href',
               'LZN' : '//div[@class="pagination"]/a/@href',
               'ZZZ' : "//a[@class='nextpostslink']/@href",
               'Z800' : '//span[@class="next"]/a/@href',
               '91TH' : '//a[@class="nextpostslink"]/@href',
               'TSDXB' : '//div[@class="pagen"]/a/@href',
               'HH' : '//a[@class="js-log pager-next"]/@href',
               'TZ' : '//a[@class="next"]/@href',
               'FXZDM' : "//a[@class='nextpostslink']/@href",
               'PYD' : '//a[@class="nextpostslink"]/@href',
               'YHYH' : "//a[@class='nextpostslink']/@href",
               'CZFXH' : "//a[@class='nextpostslink']/@href",
               'DWM' : 'NONE',
               'MSMPY' : "//link[@rel='next']/@href",
               'QG' : '//font[@class="pageUD"]/a/@href',
               'WABCW' : "//a[@class='nextpostslink']/@href",
               '5TAO' : 'NONE',
               'TDPYH' : '//div[@class="page"]/a/@href',
               'MTYHD' : '//a[@class="nextpostslink"]/@href',
               'MGPYH' : '//a[@class="pure-button next"]/@href',
               'SMZDT' : '//div[@class="page_navi"]/a/@href',
               '360ZDM' : "//a[@class='nextpostslink']/@href"},
'NEXT_PAGE_INDEX' : {'SMZDM' : -1,
                'LZN' : -1,
                'ZZZ' : -1,
                'Z800' : -1,
                '91TH' : -1,
                'TSDXB' : -1,
                'HH' : -1,
                'TZ' : -1,
                'FXZDM' : -1,
                'PYD' : -1,
                'YHYH' : -1,
                'CZFXH' : -1,
                'DWM' : -1,
                'MSMPY' : -1,
                'QG' : -1,
                'WABCW' : -1,
                '5TAO' : -1,
                'TDPYH' : -1,
                'MTYHD' : -1,
                'MGPYH' : -1,
                'SMZDT' : -2,
                '360ZDM' : -1},
'DESC_MAIN_PATH' : {'SMZDM' : '//div[@class="perContentBox"]',
                    'LZN' : '//div[@class="detail_content"]',
                    'ZZZ' : '//div[@class="content"]',
                    'Z800' : '//div[@id="contentA"]',
                    '91TH' : '//div[@class="post_content"]',
                    'TSDXB' : '//div[@class="l_bk"]',
                    'HH' : '//div[@id="item-detail"]',
                    'TZ' : '//div[@id="Content_detail"]',
                    'FXZDM' : '//div[@class="entry lazyload"]',
                    'PYD' : '//div[@class="post_content"]',
                    'YHYH' : '//div[@class="post clearfix"]',
                    'CZFXH' : '//div[@class="post"]',
                    'DWM' : '//div[@class="boxes boxesext entry"]',
                    'MSMPY' : '//div[@class="conBox"]',
                    'QG' : '//div[@class="r"]',
                    'WABCW' : '//div[@class="entry"]',
                    '5TAO' : '//div[@class="entry"]',
                    'TDPYH' : '//div[@class="conBox"]',
                    'MTYHD' : '//div[@class="post_content"]',
                    'MGPYH' : '//div[@class="post-detail"]',
                    'SMZDT' : '//div[@class="article_content"]',
                    '360ZDM' : '//div[@class="entry"]'},
'DESC_PATH' : {'SMZDM' : ['//p[@class="p_excerpt"]','//p[@class="p_detail"]'],
               'LZN' : ['//div[@class="detail_inner"]/p'],
               'ZZZ' : ['//div[@class="content_text"]/p'],
               'Z800' : ['//div[@class="info"]/p'],
               '91TH' : ['p'],
               'TSDXB' : ['.//p'],
               'HH' : ['//p[@class="Strategy-indent-p editer-content"]','//p[@class="Strategy-p editer-content"]'],
               'TZ' : ['.//p'],
               'FXZDM' : ['.//p'],
               'PYD' : ['p'],
               'YHYH' : ['//div[@class="single_page_content"]/p'],
               'CZFXH' : ['div[@class="content"]/p'],
               'DWM' : ['//div[class="standardfontsize textblock"]/p'],
               'MSMPY' : ['p'],
               'QG' : ['p'],
               'WABCW' : ['p'],
               '5TAO' : ['p'],
               'TDPYH' : ['p'],
               'MTYHD' : ['p'],
               'MGPYH' : ['p'],
               'SMZDT' : ['.//p'],
               '360ZDM' : ['p']},
'DESC_LINK_URL' : {'SMZDM' : './/a/@href',
                       'LZN' : './/a/@href',
                       'ZZZ' : './/a/@href',
                       'Z800' : './/a/@href',
                       '91TH' : './/a/@href',
                       'TSDXB' : './/a/@href',
                       'HH' : './/a/@href',
                       'TZ' : './/a/@href',
                       'FXZDM' : './/a/@href',
                       'PYD' : './/a/@href',
                       'YHYH' : 'NONE',
                       'CZFXH' : './/a/@href',
                       'DWM' : './/a/@href',
                       'MSMPY' : './/a/@href',
                       'QG' : 'NONE',
                       'WABCW' : './/a/@href',
                       '5TAO' : './/a/@href',
                       'TDPYH' : './/a/@href',
                       'MTYHD' : './/a/@href',
                       'MGPYH' : './/a/@href',
                       'SMZDT' : './/a/@href',
                       '360ZDM' : './/a/@href'},
'DESC_LINK_CONTENT' : {'SMZDM' : './/a/@href',
                   'LZN' : './/a/text()',
                   'ZZZ' : './/a/text()',
                   'Z800' : './/a/text()',
                   '91TH' : './/a/span/text()',
                   'TSDXB' : './/a/span/text()',
                   'HH' : './/a/text()',
                   'TZ' : './/a/text()',
                   'FXZDM' : './/a/text()',
                   'PYD' : './/a/strong/text()',
                   'YHYH' : 'NONE',
                   'CZFXH' : './/a/text()',
                   'DWM' : './/a/text()',
                   'MSMPY' : './/a/strong/text()',
                   'QG' : 'NONE',
                   'WABCW' : './/a/text()',
                   '5TAO' : './/a/text()',
                   'TDPYH' : './/a/text()',
                   'MTYHD' : './/a/text()',
                   'MGPYH' : './/a/text()',
                   'SMZDT' : './/a/text()',
                   '360ZDM' : './/a/text()'},
'GO_LINK_PATH' : {'SMZDM' : ['//div[@class="zhida"]/a/@href','//div[@class="zhida_more"]/a/@href','//div[@class="zhida_more"]/div/a/@href'],
                 'LZN' : ['//a[@class="goto_link"]/@href'],
                 'ZZZ' : ['//div[@class="content_box_gobuy"]/a/@href'],
                 'Z800' : ['.//div[@class="l"]/span/a/@href'],
                 '91TH' : ['//div[@class="buy"]/a/@href'],
                 'TSDXB' : ['//div[@class="buy_right"]/a/@href'],
                 'HH' : ['//div[@class="huili-relevant-left"]/a/@href'],
                 'TZ' : ['//a[@class="btn_buy"]/@href'],
                 'FXZDM' : ['//div[@id="shop_url"]/a/@href'],
                 'PYD' : ['//div[@class="buy"]/a/@href'],
                 'YHYH' : ['//div[@class="buy_url_single"]/a/@href'],
                 'CZFXH' : ['//div[@class="buy_button"]/a/@href'],
                 'DWM' : ['NONE'],
                 'MSMPY' : ['//div[@class="zhida"]/a/@href'],
                 'QG' : ['span[@class="comments_view"]/a/@href'],
                 'WABCW' : ['NONE'],
                 '5TAO' : ['//div[@class="entry"]/p/.//a/@href'],
                 'TDPYH' : ['//div[@class="zhida_more"]/a/@href'],
                 'MTYHD' : ['//div[@class="buy"]/a/@href'],
                 'MGPYH' : ['//div[@class="thumb"]/a/@href'],
                 'SMZDT' : ['NONE'],
                 '360ZDM' : ['//div[@class="buy_url"]/a/@href']},
#'DESC_IMG_PATH' : {'SMZDM' : 'img/@src',
#                   'LZN' : 'a/img/@src',
#                   'ZZZ' : 'img/@src',
#                   'Z800' : 'NONE',
#                   '91TH' : 'img/@src',
#                   'TSDXB' : 'NONE',
#                   'HH' : 'NONE',
#                   'TZ' : 'NONE',
#                   'FXZDM' : 'a/img/@src',
#                  'PYD' : 'img/@src',
#                   'YHYH' : 'img/@src',
#                   'CZFXH' : 'img/@src',
#                   'DWM' : 'img/@src',
#                   'MSMPY' : 'a/img/@src',
#                   'QG' : 'NONE',
#                   'WABCW' : 'img/@src',
#                   '5TAO' : 'img/@src',
#                   'TDPYH' : 'img/@src',
#                   'MTYHD' : 'img/@src',
#                   'MGPYH' : 'NONE',
#                   'SMZDT' : 'img/@src',
#                   '360ZDM' : 'a/img/@src',
#                   'ETAO' : 'img/@src'},
'DESC_IMG_PATH' : {'SMZDM' : 'NONE',
                   'LZN' : 'NONE',
                   'ZZZ' : 'img/@src',
                   'Z800' : 'NONE',
                   '91TH' : 'NONE',
                   'TSDXB' : 'NONE',
                   'HH' : 'NONE',
                   'TZ' : 'NONE',
                   'FXZDM' : '/img/@src',
                   'PYD' : 'NONE',
                   'YHYH' : 'NONE',
                   'CZFXH' : 'NONE',
                   'DWM' : 'img/@src',
                   'MSMPY' : 'NONE',
                   'QG' : 'NONE',
                   'WABCW' : 'img/@src',
                   '5TAO' : 'img/@src',
                   'TDPYH' : 'NONE',
                   'MTYHD' : 'NONE',
                   'MGPYH' : 'NONE',
                   'SMZDT' : 'img/@src',
                   '360ZDM' : 'a/img/@src'},
'IMG_PATH' : {'SMZDM' : '//div[@class="conRightPic"]/a/img/@src',
              'LZN' : '//div[@class="detail_img"]/a/img/@src',
              'ZZZ' : 'NONE',
              'Z800' : '//div[@class="info"]/img/@src',
              '91TH' : '//div[@class="thumb"]/img/@src',
              'TSDXB' : '//div[@class="r_bk_imgn"]/a/img/@src',
              'HH' : '//div[@class="Strategy-pic"]/img/@src',
              'TZ' : '//a[@class="post_thumb_pic"]/img/@src',
              'FXZDM' : './/img/@src',
              'PYD' : '//div[@class="thumb"]/img/@src',
              'YHYH' : '//div[@class="post_thumb"]/a/img/@src',
              'CZFXH' : '//div[@class="post_thumb"]/a/img/@src',
              'DWM' : 'NONE',
              'MSMPY' : '//div[@class="pro_img"]/img/@src',
              'QG' : '//div[@class="l"]/img/@src',
              'WABCW' : 'NONE',
              '5TAO' : 'NONE',
              'TDPYH' : '//div[@class="pro_img"]/a/img/@src',
              'MTYHD' : '//div[@class="thumb"]/img/@src',
              'MGPYH' : '//div[@class="thumb"]/img/@src',
              'SMZDT' : 'NONE',
              '360ZDM' : 'NONE'},
'CAT_PATH' : {'SMZDM' : '//div[@class="classified"]/a/text()',
              'LZN' : '//div[@class="other_info"]/a[@class="pub_cat"]/text()',
              'ZZZ' : '//a[@rel="category tag"]/text()',
              'Z800' : './/div[@class="r"]/h4/a/text()',
              '91TH' : '//span[@class="cates"]/a/text()',
              'TSDXB' : '//div[@class="sc_sj"]/a/text()',
              'HH' : '//a[@class="hico-doc hico-cagegory js-log"]/text()',
              'TZ' : '//div[@class="tags clearfix"]/a/text()',
              'FXZDM' : 'NONE',
              'PYD' : '//span[@class="cates"]/a/text()',
              'YHYH' : 'NONE',
              'CZFXH' : 'NONE',
              'DWM' : 'NONE',
              'MSMPY' : '//span[@class="has_from_val classified"]/a/text()',
              'QG' : '//span[@class="tag"]/a/text()',
              'WABCW' : '//div[@class="postmetadata"]/a/text()',
              '5TAO' : 'NONE',
              'TDPYH' : '//a[@rel="category tag"]/text()',
              'MTYHD' : '//span[@class="cates"]/a/text()',
              'MGPYH' : '//div[@class="pull-left"]/a/text()',
              'SMZDT' : '//a[@rel="category tag"]/text()',
              '360ZDM' : 'NONE'},
'SOURCE_PATH' : {'SMZDM' : './/span[@class="from_val"]/text()',
                 'LZN' : '//div[@class="other_info"]/a[@class="pub_shop"]/text()',
                 'ZZZ' : 'NONE',
                 'Z800' : 'h3/span/a/text()',
                 '91TH' : "//div[@class='mall']/a/text()",
                 'TSDXB' : '//div[@class="sc_sj"]/a/text()',
                 'HH' : 'NONE',
                 'TZ' : '//span[@class="created"]/a/text()',
                 'FXZDM' : 'NONE',
                 'PYD': "//div[@class='mall']/a/text()",
                 'YHYH' : 'NONE',
                 'CZFXH' : 'NONE',
                 'DWM' : 'NONE',
                 'MSMPY' : './/span[@class="from_val"]/text()',
                 'QG' : '//span[@class="mall"]/text()',
                 'WABCW' : 'NONE',
                 '5TAO' : 'NONE',
                 'TDPYH' : '//span[@class="from_val"]/text()',
                 'MTYHD' : '//div[@class="mall"]/a/text()',
                 'MGPYH' : 'NONE',
                 'SMZDT' : 'NONE',
                 '360ZDM' : 'NONE'},
'WORTH_SCORE_PATH' : {'SMZDM' : '//div[@class="worth_1"]/a/text()',
                      'LZN' : '//span[@class="worth_num"]/text()',
                      'ZZZ' : 'NONE',
                      'Z800' : 'NONE',
                      '91TH' : '//span[@class="vote_up"]/a/span/text()',
                      'TSDXB' : 'NONE',
                      'HH' : 'NONE',
                      'TZ' : 'NONE',
                      'FXZDM' : 'NONE',
                      'PYD' : 'NONE',
                      'YHYH' : 'NONE',
                      'CZFXH' : 'NONE',
                      'DWM' : 'NONE',
                      'MSMPY' : 'NONE',
                      'QG' : 'NONE',
                      'WABCW' : 'NONE',
                      '5TAO' : 'NONE',
                      'TDPYH' : 'NONE',
                      'MTYHD' : 'NONE',
                      'MGPYH' : 'NONE',
                      'SMZDT' : 'NONE',
                      '360ZDM' : 'NONE'},
'BAD_SCORE_PATH' : {'SMZDM' : '//div[@class="worth_3"]/a/text()',
                    'LZN' : '//span[@class="noworth_num"]/text()',
                    'ZZZ' : 'NONE',
                    'Z800' : 'NONE',
                    '91TH' : '//span[@class="vote_down"]/a/span/text()',
                    'TSDXB' : 'NONE',
                    'HH' : 'NONE',
                    'TZ' : 'NONE',
                    'FXZDM' : 'NONE',
                    'PYD' : 'NONE',
                    'YHYH' : 'NONE',
                    'CZFXH' : 'NONE',
                    'DWM' : 'NONE',
                    'MSMPY' : 'NONE',
                    'QG' : 'NONE',
                    'WABCW' : 'NONE',
                    '5TAO' : 'NONE',
                    'TDPYH' : 'NONE',
                    'MTYHD' : 'NONE',
                    'MGPYH' : 'NONE',
                    'SMZDT' : 'NONE',
                    '360ZDM' : 'NONE'},
'NEED_FILTER' : {'SMZDM':1,
                 'LZN':1,
                 'ZZZ':0,
                 'Z800':0,
                 '91TH':1,
                 'TSDXB' : 0,
                 'HH' : 0,
                 'TZ' : 0,
                 'FXZDM' : 0,
                 'PYD' : 1,
                 'YHYH' : 0,
                 'CZFXH' : 0,
                 'DWM' : 0,
                 'MSMPY' : 1,
                 'QG' : 0,
                 'WABCW' : 0,
                 '5TAO' : 0,
                 'TDPYH' : 0,
                 'MTYHD' : 0,
                 'MGPYH' : 0,
                 'SMZDT' : 0,
                 '360ZDM' : 0}
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Smzdm (+http://www.yourdomain.com)'
