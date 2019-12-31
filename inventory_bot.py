from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException



import time
import sys
from collections import defaultdict

password = "*****"
wait_time = 1

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.implicitly_wait(10)

size_dict = {
    "3.5":"3.5Y / 5W",
    "4":"4Y / 5.5W",
    "4.5":"4.5Y / 6W",
    "5":"5Y / 6.5W",
    "5.5":"5.5Y / 7W",
    "6":"6Y / 7.5W",
    "6.5":"6.5Y / 8W",
    "7Y":"7Y",
    "7.5Y":"7.5Y",
    "7":"7M / 8.5W",
    "7.5":"7.5M / 9W",
    "8":"8M / 9.5W",
    "8.5":"8.5M / 10W",
    "9":"9M / 10.5W",
    "9.5":"9.5M / 11W",
    "10":"10M / 11.5W",
    "11":"11M",
    "11.5":"11.5M",
    "12":"12M",
    "12.5":"12.5M",
    "13":"13M",
    "14":"14M",
    "15":"15M"
}

test_size_dict = {
    "7.5":"7.5T",
    "8":"8T",
    "9":"9T",
    "10":"10T",
    "11":"11T"
}

class Shoe:
    def __init__(self, sku, retail_price, name, stock):
        self.sku = sku
        self.retail_price = retail_price
        self.name = name
        self.stock = stock

    def input_shoe(self, size_name):

        time.sleep(wait_time)
        driver.find_element_by_xpath("//*[@title='Add Product']").click()
        driver.find_element_by_xpath("//*[@data-value='store-item-physical']").click()
        driver.find_element_by_name("title").send_keys(self.name+" "+size_name)
        description = "Retail: $"+self.retail_price+".00\nSKU: "+self.sku
        driver.find_element_by_class_name("RichTextField-editor-irMem").send_keys(description)

        if self.stock > 1:
            driver.find_elements_by_class_name("TabbedHeader-tab-2kGQy")[1].click()
            time.sleep(wait_time)
            driver.find_element_by_name("stock").click()
            # try:
            #     driver.find_element_by_name("stock").click()
            # except ElementClickInterruptedException:
            #     time.sleep(3)
            #     driver.find_element_by_name("stock").click()


            qty_field = driver.find_element_by_name("qtyInStock")
            qty_field.send_keys(Keys.BACKSPACE)
            qty_field.send_keys(self.stock)

        time.sleep(wait_time)

        driver.find_element_by_class_name("saveAndClose").click()
        print("added "+self.sku+": "+self.name + " stock: "+str(self.stock))
        time.sleep(wait_time)
        driver.refresh()



#parse file

if len(sys.argv) < 2:
    print("error, must run with filename")
    sys.exit(0)
    driver.quit()
if len(sys.argv)==3 and sys.argv[2]=="test":
    print("will enter shoes into test sizes")
    run_dict = test_size_dict
else:
    run_dict = size_dict


f = open("input-files/"+ sys.argv[1])
shoe_dict = defaultdict(list)
for x in f:
    details = x.rstrip("\n").split(",")
    if len(details) < 4:
        print("sku number " + detail[0] + "is not formatted correctly")
    stock_dict = defaultdict(int)
    for i in range(3, len(details)):
        stock_dict[details[i]] += 1

    for y in stock_dict:
        shoe_dict[y].append(Shoe(sku = details[0], retail_price=details[1], name = details[2], stock=stock_dict[y]))


for size_num in shoe_dict:
    print(size_num)
    sneaker_list = shoe_dict[size_num]
    for sneaker in sneaker_list:
        print(sneaker.name+" stock: "+str(sneaker.stock))
    print(" ")

#input data sorted by shoe, resorted to  by size
f.close()




driver.get("http://www.squarespace.com")

#disabled automated login to bypass recaptcha

#login_button = driver.find_element_by_class_name("www-navigation__desktop__account-info__login-button")
#login_button.click()

#email_field = driver.find_element_by_name("email")
#pass_field = driver.find_element_by_name("password")

#email_field.send_keys("client-email@gmail.com")
#pass_field.send_keys(password)
time.sleep(15)

#pass_field.send_keys(Keys.ENTER)

driver.find_element_by_class_name("styles-card-3S47l").click()
time.sleep(3)
driver.find_element_by_xpath("//*[@data-test='menuItem-pages']").click()


try:
    for each_size in shoe_dict:
        if each_size not in run_dict:
            print("cannot find size "+each_size+" in squarespace page\n")
        else:
            size_title = run_dict[each_size]
            print("adding shoes in size "+size_title)
            time.sleep(wait_time)
            driver.find_element_by_xpath("//*[@title='" +size_title+ "']").click()
            for each_shoe in shoe_dict[each_size]:
                each_shoe.input_shoe(size_title.replace(" ", ''))
            print(" ")
            driver.find_element_by_xpath("//*[@data-test='menuHeader-back']").click()

except NoSuchElementException:
    print("program crashed. try increasing wait time")
    driver.quit()


print("program finished")
time.sleep(60)


driver.quit()
