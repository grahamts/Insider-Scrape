from selenium import webdriver
import csv
import time

start_time = time.time()
outfile = open("IndiaInsiderTransactions.csv", 'w')
writer = csv.writer(outfile)
url = 'http://www.bseindia.com/corporates/Insider_Trading_new.aspx?expandable=2'
driver = webdriver.Firefox()

driver.get(url)

try:
    page_parent = driver.find_element_by_xpath('//*[@id="gvData"]/tbody/tr[28]/td/table/tbody/tr')
    num_pages = len(page_parent.find_elements_by_tag_name('td'))
except:
    num_pages = 1

print("Total pages to scrape: " + str(num_pages))
# Scrapes data row by row, page by page
for i in range(2, num_pages+2):
    table_parent = driver.find_element_by_xpath('//*[@id="gvData"]/tbody')
    num_rows = len(table_parent.find_elements_by_tag_name('tr'))
    print('Scraping page ' + str(i-1) + '...')
    for j in range(3,num_rows-1):
        write_list=[]
        for k in range(1,13):
            write_list.append(driver.find_element_by_xpath('//*[@id="gvData"]/tbody/tr[' + str(j) +']/td[' + str(k) + ']').text)
            
        if write_list[11] == 'ESOP':
            continue
        
        if ' ' in write_list[10]:
            part_one = write_list[10][0:write_list[10].index(" ")]
            part_two = write_list[10][write_list[10].index(" ") + 1:len(write_list[10])]
        else:
            part_one = write_list[10]
            part_two = ' '  
        
        try:
            if int(write_list[4][:write_list[4].index('(')]) > int(write_list[9][:write_list[9].index('(')]):
                write_list.append('S')
            else:
                write_list.append('B')
        except:
            write_list.append('')
        
        write_tuple = tuple(write_list)
        print(write_tuple)
        
        writer.writerow([write_tuple[0], write_tuple[1], write_tuple[2], write_tuple[3], part_one + ' - ' + part_two, part_one, write_tuple[12], 
                         write_tuple[11], write_tuple[6].replace(',',''), '', write_tuple[9], '', 
                         write_tuple[9][write_tuple[9].index("(") + 1:write_tuple[9].rindex(")")], '', ''])
        
    if i < num_pages+1:
        driver.find_element_by_xpath('//*[@id="gvData"]/tbody/tr[28]/td/table/tbody/tr/td[' + str(i) + ']/a').click()
        
print('Done')
driver.quit()
print('Elapsed time: ' + str(time.time()-start_time))



