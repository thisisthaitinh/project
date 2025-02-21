# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import os



class MyprojectPipeline:
    def process_item(self, item, spider):
        return item
    
class MySQLPipeline:
    def open_spider(self, spider):
        self.connection = pymysql.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', 'Thaitinh2004!'),
            db=os.getenv('MYSQL_DATABASE', 'crawled_data'),
            cursorclass=pymysql.cursors.DictCursor
        )

        self.cursor = self.connection.cursor()

        if spider.name == 'site1_crawler':
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS CHAMPIONS_LEAGUE_RESULTS (
                id INT AUTO_INCREMENT PRIMARY KEY,
                NGAY_THI_DAU VARCHAR(255),  
                TRANG_THAI VARCHAR(255),
                DOI_NHA VARCHAR(255),
                TI_SO VARCHAR(255),
                DOI_KHACH VARCHAR(255),
                LINK_BAI_VIET VARCHAR(255)
            )
        ''')
        elif spider.name == 'site2_crawler':
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS DAN_TRI_NEWS (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                TIEU_DE VARCHAR(255),
                MO_TA VARCHAR(255),
                THOI_GIAN VARCHAR(255),
                TAC_GIA VARCHAR(255),
                LINK VARCHAR(255)
            )
        ''')
        elif spider.name == 'site3_crawler':
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS BAT_DONG_SAN (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                TIEU_DE VARCHAR(255),
                DIA_CHI VARCHAR(255),
                DIEN_TICH VARCHAR(255),
                MUC_GIA VARCHAR(255),
                THONG_TIN_CHI_TIET VARCHAR(255),
                LINK_BAI_VIET VARCHAR(255)
            )
        ''')
        elif spider.name == 'site4_crawler':
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS THONG_TIN_VIEC_LAM (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                TEN_CONG_VIEC VARCHAR(255),
                TEN_CONG_TY VARCHAR(255),
                MUC_LUONG VARCHAR(255),
                DIA_DIEM VARCHAR(255),
                LINK_BAI_VIET VARCHAR(255)
            )
        ''')
        

    def process_item(self, item, spider):
        if spider.name == 'site1_crawler':
            self.cursor.execute(
                "INSERT INTO CHAMPIONS_LEAGUE_RESULTS (NGAY_THI_DAU, TRANG_THAI, DOI_NHA, TI_SO, DOI_KHACH, LINK_BAI_VIET) VALUES (%s, %s, %s, %s, %s, %s)",
                (item['ngay_thi_dau'], item['trang_thai'], item['doi_nha'], item['ti_so'], item['doi_khach'], item['url'])
            )
        elif spider.name == 'site2_crawler':
            self.cursor.execute(
                "INSERT INTO DAN_TRI_NEWS (TIEU_DE, MO_TA, THOI_GIAN, TAC_GIA, LINK) VALUES (%s, %s, %s, %s, %s)",
                (item['title'], item['description'], item['posted_time'], item['author'], item['link'])
            )
        elif spider.name == 'site3_crawler':
            self.cursor.execute(
                "INSERT INTO BAT_DONG_SAN (TIEU_DE, DIA_CHI, DIEN_TICH, MUC_GIA, THONG_TIN_CHI_TIET, LINK_BAI_VIET) VALUES (%s, %s, %s, %s, %s, %s)",
                (item['title'], item['location'], item['area'], item['price'], item['details'], item['url'])
            )
        elif spider.name == 'site4_crawler':
            self.cursor.execute(
                "INSERT INTO THONG_TIN_VIEC_LAM (TEN_CONG_VIEC, TEN_CONG_TY, MUC_LUONG, DIA_DIEM, LINK_BAI_VIET) VALUES (%s, %s, %s, %s, %s)",
                (item['job_title'], item['company_name'], item['salary'], item['location'], item['url'])
            )
            
        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

