from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np
import time
from time import sleep
from datetime import datetime
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()


now = (datetime.now())
run_datetime = now.strftime("%Y/%m/%d %H:%M:%S")
print(run_datetime)

start_time = time.time()

today = datetime.today().strftime('%Y%m%d')
date = str(today)


url = "https://www.consumerreports.org/global/login"

options = webdriver.ChromeOptions()

# Set user agent
# user_agent = 'userMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
# options.add_argument(f'user-agent={user_agent}')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--no-sandbox')
# options.add_argument('-headless')

driver = webdriver.Chrome()


driver.get(url)
driver.find_element(By.NAME, "userName").send_keys(os.getenv("username"))
driver.find_element(By.NAME, "password").send_keys(os.getenv("password"))
sleep(2)
driver.find_element(By.CSS_SELECTOR, "input[type=\"submit\" i]").click()
sleep(2)
print('login success')
sleep(2)



def scrape_cr_ranking(rows):
    results = []
    for row in rows:
        category = row.find_element(By.XPATH, ".//*[@class='shared-crux-label crux-label-style crux-label-style--small crux-primary-gray']").text
        model = row.find_element(By.XPATH, ".//*[contains(@class, 'crux-component-title list__model')]").text
        price = row.find_element(By.XPATH, ".//*[contains(@class, 'shared-crux-text crux-body-copy')]").text
        overall_score = row.find_element(By.XPATH, ".//*[contains(@class, 'crux-overall-score--lg')]").text
        # print(model)
        # print(overall_score)
        # overall_score = row.find_element(By.XPATH, ".//*[contains(@class, 'crux-overall-score-static crux-color-excellent-bg crux-overall-score--lg']").text

        data = {
            'category': category,
            'datetime': run_datetime,
            'model': model,
            'price': price,
            'overall_score': overall_score,

        }

        results.append(data)

    return results

def reorganize(df, var1, var2, var3, var4):
    df.insert(2, var1, range(1, 1 + len(df)))
    df.insert(0, var3, range(1, 1 + len(df)))
    df.dropna(axis=1, how='all', inplace=True)
    for r in df.iterrows(): # If scores are the same, give the same ranking
        df[var1] = np.where(df[var2] == df[var2].shift(1), df[var1].shift(1), df[var1])
        df[var1] = df[var1].astype(int)
        df[var3] = var4

    return df

product_categories_url = [
    ['https://www.consumerreports.org/products/vacuum-cleaners-28984/cordless-stick-vacuums-200448/view1/','STICK VACUUM', 'Cordless Stick Vacuum'],
    ['https://www.consumerreports.org/products/vacuum-cleaners-28984/robotic-vacuum-35183/view1/','ROBOT VACUUM','Robot Vacuum'],
    ['https://www.consumerreports.org/products/ranges-28974/gas-range-28694/view1/#subtypes%3A31038%3B','GAS RANGE','Gas Range (Single)'],
    ['https://www.consumerreports.org/products/ranges-28974/gas-range-28694/view1/#subtypes%3A31036%3B','GAS RANGE','Gas Range (Double)'],
    ['https://www.consumerreports.org/products/ranges-28974/electric-range-28689/view1/#subtypes%3A31012%3B','ELECTRIC RANGE', 'Elec Range (Single)'],
    ['https://www.consumerreports.org/products/ranges-28974/electric-range-28689/view1/#subtypes%3A31013%3B','ELECTRIC RANGE', 'Elec Range (Double)'],
    ['https://www.consumerreports.org/products/ranges-28974/electric-induction-ranges-37181/view1/','INDUCTION RANGE', 'Elec Range (Induction)', 'Elec Range (Induction)'],
    ['https://www.consumerreports.org/products/wall-ovens-200189/electric-wall-ovens-28738/view1/#subtypes%3A33264%3B','ELECTRIC WALL OVEN', 'Wall Oven (Single)' ],
    ['https://www.consumerreports.org/products/wall-ovens-200189/electric-wall-ovens-28738/view1/#subtypes%3A35189%3B','ELECTRIC WALL OVEN', 'Wall Oven (Double)' ],
    ['https://www.consumerreports.org/products/microwave-ovens-28973/countertop-microwave-oven-28706/view1/#subtypes%3A200166%3B','COUNTERTOP MICROWAVE', 'Microwave (Small)'],
    ['https://www.consumerreports.org/products/microwave-ovens-28973/countertop-microwave-oven-28706/view1/#subtypes%3A30245%3B','COUNTERTOP MICROWAVE', 'Microwave (Midsized)'],
    ['https://www.consumerreports.org/products/microwave-ovens-28973/countertop-microwave-oven-28706/view1/#subtypes%3A30247%3B','COUNTERTOP MICROWAVE', 'Microwave (Large)'],
    ['https://www.consumerreports.org/products/microwave-ovens-28973/over-the-range-microwave-oven-32000/view1/','OTR MICROWAVE', 'Microwave (OTR)'],
    ['https://www.consumerreports.org/products/air-conditioners-28969/air-conditioner-28666/view1/#subtypes%3A30705%3B','WINDOW AIR CONDITIONER', 'Window Air Conditioners (5000-6500 BTU/hr)'],
    ['https://www.consumerreports.org/products/air-conditioners-28969/air-conditioner-28666/view1/#subtypes%3A30706%3B','WINDOW AIR CONDITIONER', 'Window Air Conditioners (7000-8500 BTU/hr)'],
    ['https://www.consumerreports.org/products/air-conditioners-28969/air-conditioner-28666/view1/#subtypes%3A30704%3B','WINDOW AIR CONDITIONER', 'Window Air Conditioners (9800-12500 BTU/hr)'],
    ['https://www.consumerreports.org/products/air-conditioners-28969/portable-air-conditioners-37010/view1/','PORTABLE AIR CONDITIONER', 'Portable Air Conditioners'],
    ['https://www.consumerreports.org/products/air-purifiers-29549/room-air-purifier-29550/view1/','ROOM AIR PURIFIER', 'Air Purifiers'],
    ['https://www.consumerreports.org/products/dehumidifiers-33019/dehumidifier-33010/view1/#subtypes%3A33168%3B','DEHUMIDIFIER', 'Dehumidifiers (Large)'],
    ['https://www.consumerreports.org/products/dehumidifiers-33019/dehumidifier-33010/view1/#subtypes%3A33170%3B','DEHUMIDIFIER', 'Dehumidifiers (Medium)'],
    ['https://www.consumerreports.org/products/dehumidifiers-33019/dehumidifier-33010/view1/#subtypes%3A33169%3B','DEHUMIDIFIER', 'Dehumidifiers (Small)'],
    ['https://www.consumerreports.org/products/refrigerators-28978/top-freezer-refrigerator-28722/view1/#subtypes%3A200379%3B','TOP-FREEZER REFRIGERATOR', 'Refrigerators (Top) 29-30 inch'],
    ['https://www.consumerreports.org/products/refrigerators-28978/top-freezer-refrigerator-28722/view1/#subtypes%3A200380%3B','TOP-FREEZER REFRIGERATOR', 'Refrigerators (Top) 31 inch and wider'],
    ['https://www.consumerreports.org/products/refrigerators-28978/bottom-freezer-refrigerator-28719/view1/#subtypes%3A200373%3B','BOTTOM-FREEZER REFRIGERATOR', 'Refrigerators (Bottom) 30 inch and narrower'],
    ['https://www.consumerreports.org/products/refrigerators-28978/bottom-freezer-refrigerator-28719/view1/#subtypes%3A200375%3B','BOTTOM-FREEZER REFRIGERATOR', 'Refrigerators (Bottom) 31-33 inch'],
    ['https://www.consumerreports.org/products/refrigerators-28978/french-door-refrigerator-37162/view1/#subtypes%3A200367%3B','FRENCH-DOOR REFRIGERATOR', 'Refrigerators (French) 30 inch or narrower'],
    ['https://www.consumerreports.org/products/refrigerators-28978/french-door-refrigerator-37162/view1/#subtypes%3A200369%3B','FRENCH-DOOR REFRIGERATOR', 'Refrigerators (French) 31-33 inch'],
    ['https://www.consumerreports.org/products/refrigerators-28978/french-door-refrigerator-37162/view1/#subtypes%3A200371%3B','FRENCH-DOOR REFRIGERATOR', 'Refrigerators (French) 34 inch or wider'],
    ['https://www.consumerreports.org/products/refrigerators-28978/side-side-refrigerator-28721/view1/#subtypes%3A200364%3B','SIDE-BY-SIDE REFRIGERATOR', 'Refrigerators (SideBySide) 34 and wider'],
    ['https://www.consumerreports.org/products/washing-machines-28983/front-load-washer-28739/view1/','WASHING MACHINES', 'Washing Machines (Front-Load)'],
    ['https://www.consumerreports.org/products/washing-machines-28983/top-load-agitator-washer-32002/view1/','WASHING MACHINES', 'Washing Machines (TOP-LOAD-AGITATOR)'],
    ['https://www.consumerreports.org/products/washing-machines-28983/top-load-he-washer-37107/view1/','WASHING MACHINES', 'Washing Machines (TOP-LOAD-HE)'],
    ['https://www.consumerreports.org/products/washing-machines-28983/compact-washers-37106/view1/','WASHING MACHINES', 'Washing Machines (COMPACT)'],
    ['https://www.consumerreports.org/products/clothes-dryers-28982/electric-dryer-30562/view1/','CLOTHES DRYERS', 'Dryers (Electric)'],
    ['https://www.consumerreports.org/products/clothes-dryers-28982/gas-dryer-30563/view1/','CLOTHES DRYERS', 'Dryers (Gas)'],
    ['https://www.consumerreports.org/products/clothes-dryers-28982/compact-dryers-37294/view1/','CLOTHES DRYERS', 'Dryers (Compact)'],
    ['https://www.consumerreports.org/products/dishwashers-28979/dishwasher-28687/view1/#subtypes%3A33347%3B','DISHWASHERS', 'Dishwashers (24-INCH)'],
    ['https://www.consumerreports.org/products/cooktops-28977/electric-smoothtop-cooktops-28688/view1/#subtypes%3A30989%3B','ELECTRIC COOKTOPS', 'ELECTRIC COOKTOPS (30-INCH)'],
    ['https://www.consumerreports.org/products/cooktops-28977/electric-smoothtop-cooktops-28688/view1/#subtypes%3A30998%3B','ELECTRIC COOKTOPS', 'ELECTRIC COOKTOPS (36-INCH)'],
    ['https://www.consumerreports.org/products/cooktops-28977/electric-induction-cooktops-200764/view1/#subtypes%3A200765%3B','INDUCTION COOKTOPS', 'INDUCTION COOKTOPS (30-INCH)'],
    ['https://www.consumerreports.org/products/cooktops-28977/electric-induction-cooktops-200764/view1/#subtypes%3A200766%3B','INDUCTION COOKTOPS', 'INDUCTION COOKTOPS (36-INCH)'],
    ['https://www.consumerreports.org/products/cooktops-28977/gas-cooktop-28692/view1/#subtypes%3A30983%3B','GAS COOKTOPS', 'GAS COOKTOPS (30-INCH)'],
    ['https://www.consumerreports.org/products/cooktops-28977/gas-cooktop-28692/view1/#subtypes%3A30984%3B','GAS COOKTOPS', 'GAS COOKTOPS (36-INCH)']
 ]

def scrape_each_product_cat(url):
    driver.get(url)
    driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
    sleep(5)
    try:
        item_rows = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//*[@class='row list__row']")))
        data = scrape_cr_ranking(item_rows)
        print(len(data))
        return data
    except Exception as e:
        print(e)
        return None
    no_of_items = driver.find_element(By.XPATH, ".//*[contains(@class, 'crux-numbers--small')]").text
    if int(no_of_items) == len(data):
        return data
    else:
        raise Exception('Error: Number of results does not match number of items listed')



def create_connection():
    # establishing the connection
    conn = None
    try:
        conn = psycopg2.connect(
            database=os.getenv("database"),
            user=os.getenv("db_user"),
            password=os.getenv("db_password"),
            host=os.getenv("host"),
            port=os.getenv("port")
        )
        conn.autocommit = True
        print("Connected to database")
    except Exception as e:
        print(e)

    return conn

def delete_prev(conn):
    """ delete daily_ranking_prev table """
    cur = conn.cursor()
    cur.execute("""DROP TABLE daily_ranking_prev;""")

def insert_prev(conn):
    """ transfer current daily_ranking_daily data into the daily_ranking_prev table """
    cur = conn.cursor()
    cur.execute("""CREATE TABLE daily_ranking_prev
       (
              id serial PRIMARY KEY,
              product_group varchar,
              category varchar,
              time_checked timestamptz DEFAULT now(),
              ranking integer,
              model_name varchar,
              price varchar,
              overall_score double precision
              )
       """)

    sql = '''SELECT * FROM "daily_ranking_now"'''
    insert_query = """INSERT INTO "daily_ranking_prev" values (%s,%s,%s,%s,%s,%s,%s,%s)"""

    cur = conn.cursor()
    data = pd.read_sql_query(sql, conn)
    df_move = pd.DataFrame(data)
    cur.executemany(insert_query, df_move.values.tolist())
    conn.commit()
def delete_now(conn):
    """ delete daily_ranking_now table """
    cur = conn.cursor()
    cur.execute("""DROP TABLE daily_ranking_now;""")

def insert_now(conn):
    """
    create daily_ranking_now table and insert new data
    """

    cur = conn.cursor()
    cur.execute("""CREATE TABLE daily_ranking_now
     (
            id serial PRIMARY KEY,
            product_group varchar,
            category varchar,
            time_checked timestamptz DEFAULT now(),
            ranking integer,
            model_name varchar,
            price varchar,
            overall_score double precision
            )
     """)

    sql = """INSERT INTO "daily_ranking_now"
             ( product_group, category, time_checked, ranking, model_name, price, overall_score )
             VALUES (%s,%s,%s,%s,%s,%s,%s)"""

    for url in product_categories_url:
        data = scrape_each_product_cat(url[0])
        df = pd.concat([pd.DataFrame(data)], ignore_index=True)
        # replace '' with None
        df = df.replace(r'^\s*$', np.nan, regex=True)

        reorganize(df, 'ranking', 'overall_score', 'product_group', url[1])
        print(f'{url[1]} Complete: {df.shape}')

        cur.executemany(sql, df.values.tolist())
        conn.commit()

def insert_back(conn):
    sql = """SELECT * from daily_ranking_prev"""
    sql_insert = """INSERT INTO DailyCR_Ranking_Now
                     VALUES (%s,%s,%s,%s,%s,%s,%s)
                     ON CONFLICT (product_group, category, model_name)
                     DO UPDATE SET ranking = EXCLUDED.ranking, overall_score = EXCLUDED.overall_score, 
                     time_checked = EXCLUDED.time_checked, price = EXCLUDED.price
                     """

    cur = conn.cursor()
    data = pd.read_sql_query(sql, conn)
    df_move = pd.DataFrame(data)
    cur.executemany(sql_insert, df_move.values.tolist())
    conn.commit()


def join(conn):
    sql1 = """SELECT * from daily_ranking_now"""

    sql2 = """SELECT time_checked, product_group, category, ranking, model_name, overall_score from daily_ranking_prev"""

    # cur = conn.cursor()
    now_ranking = pd.read_sql_query(sql1, conn)
    df_now = pd.DataFrame(now_ranking)
    # Excel does not support datetimes with timezones
    df_now['time_checked'] = df_now['time_checked'].dt.strftime('%Y-%m-%d %H:%M:%S')

    prev_ranking = pd.read_sql_query(sql2, conn)
    df_prev = pd.DataFrame(prev_ranking)
    # Excel does not support datetimes with timezones
    df_prev['time_checked'] = df_prev['time_checked'].dt.strftime('%Y-%m-%d %H:%M:%S')

    df_merge = pd.merge(df_now,
                        df_prev,
                        on =['product_group','category','model_name'],
                        how ='outer'
                        )



    m = df_merge.pop('model_name')
    p = df_merge.pop('price')
    df_merge.insert(3, 'model_name', m)
    df_merge.insert(4, 'price', p)
    df_merge['k'] = df_merge['product_group'] + " " + df_merge['category']

    out, cnt = [], {}
    for r in df_merge['k']:
        if r not in cnt:
            cnt[r] = 1
            r = r + str(cnt[r])
        else:
            cnt[r] += 1
            r = r + str(cnt[r])
        out.append(r)

    df_merge['key'] = out
    c = df_merge.pop('k')
    k = df_merge.pop('key')
    df_merge.insert(1, 'concat', c)
    df_merge.insert(1, 'key', k)

    def diff(a, b):
        return a - b

    df_merge['ranking_change'] = df_merge.apply(
        lambda x: diff(x['ranking_y'], x['ranking_x']), axis=1)


    # get rid of 'from ' in price
    df_merge['price'] = df_merge['price'].str.replace('from ', '')


    print(df_merge)

    drop_tops = df_merge.drop(df_merge.groupby(['concat']).head(3).index, axis=0)
    lowRankingLG = drop_tops.loc[drop_tops['model_name'].str.contains("LG ", case=False)]
    df_LGnotop = lowRankingLG[['concat', 'ranking_x', 'model_name', 'overall_score_x']]

    cwd = os.getcwd()
    raw_path = cwd + f'/data/raw/(raw)DailyCR_{date}.csv'
    df_now.to_csv(raw_path, index=False)

    transformed_path = cwd + f'/data/transformed/(transformed)DailyCR_{date}.xlsx'

    with pd.ExcelWriter(transformed_path)as writer:
                df_merge.to_excel(writer, sheet_name='CR Raw')
                df_LGnotop.to_excel(writer, sheet_name= 'LGs Not TOP3')

    conn.commit()

def main():
    conn = create_connection()

    with conn:
        delete_prev(conn);
        insert_prev(conn);
        delete_now(conn);
        insert_now(conn);
        join(conn);
        # insert_back(conn);



if __name__ == '__main__':
    main()

print("--- %s seconds ---" % (time.time() - start_time))