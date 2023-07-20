from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

file_name = input('Do not put the extension!!! Enter filename: ')+'.txt'
disease_name = input("Enter disease's name:")
username_admin = input("Username: ")
user_password = input("Password: ")

fh = open(file_name, 'r')

PATH = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(PATH)

sust_url = 'https://bgdd.sust.edu/admin/disease/diseasecausinggene/add/'
driver.get(sust_url)

username = driver.find_element_by_css_selector("input[name='username'][class='form-control'][placeholder='Username'][required]")
username.send_keys(username_admin)

password = driver.find_element_by_name("password")
password.send_keys(user_password)

login_button = driver.find_element_by_class_name('col-12')
login_button.click()

for gene_details in fh:
    if gene_details.startswith('gene_id'):
        continue
    else: 
        gene_data_list = gene_details.split('\t')
        gene_name = gene_data_list[1]
        protein_name = gene_data_list[2]
        chromosomal_location = gene_data_list[3]
        nucleotide_accession = gene_data_list[4]
        mode_of_inheritance = gene_data_list[5]
        genecard_link = gene_data_list[6]
        kegg_link = gene_data_list[7]
        pdb_link = gene_data_list[8]
        entrez_link = gene_data_list[9]
        omim_link = gene_data_list[10]

        print(gene_name)
        print(protein_name)
        print(chromosomal_location)
        print(nucleotide_accession)
        print(mode_of_inheritance)
        print(genecard_link)
        print(kegg_link)
        print(pdb_link)
        print(entrez_link)
        print(omim_link)


        # sust url login
        sust_url = 'https://bgdd.sust.edu/admin/disease/diseasecausinggene/add/'
        driver.get(sust_url)

        # selecting disease
        disease_field = driver.find_element_by_id('select2-id_disease-container')
        disease_field.click()
        disease_field_search = driver.find_element_by_class_name('select2-search__field')
        disease_field_search.send_keys(disease_name)
        disease_field_search.send_keys(Keys.ENTER)

        # writing gene name
        gene_name_submit = driver.find_element_by_id('id_name')
        gene_name_submit.send_keys(gene_name)
        print(f'->>>>>>>>>>>> Submitting {gene_name}')

        # writing slugs
        slug_to_be_sent = gene_name.lower()
        slug_name = driver.find_element_by_name('slug')
        slug_name.clear()
        slug_name.send_keys(slug_to_be_sent)

        # writing chromosomal location
        chromosomal_location_submit = driver.find_element_by_name('chromosomal_location')
        chromosomal_location_submit.send_keys(chromosomal_location)

        # writing nucleotide accession
        nucleotide_accession_submit = driver.find_element_by_name('nucleotide_accession')
        nucleotide_accession_submit.send_keys(nucleotide_accession)

        # writing mode of inheritance
        mode_of_inheritance_submit = driver.find_element_by_name('mode_of_inheritance')
        mode_of_inheritance_submit.send_keys(mode_of_inheritance)

        # writing genecard link
        genecard_link_submit = driver.find_element_by_name('genecard_link')
        genecard_link_submit.send_keys(genecard_link)

        # writing kegg_link
        kegg_link_submit = driver.find_element_by_name('KEGG_link')
        kegg_link_submit.send_keys(kegg_link)

        # writing pdb_link
        pdb_link_submit = driver.find_element_by_name('PDB_link')
        pdb_link_submit.send_keys(pdb_link)

        # writing entrez_link
        entrez_link_submit = driver.find_element_by_name('Entrez_link')
        entrez_link_submit.send_keys(entrez_link)

        # writing omim link
        omim_link_submit = driver.find_element_by_name('OMIM_link')
        omim_link_submit.send_keys(omim_link)
        if driver.current_url != 'https://bgdd.sust.edu/admin/disease/diseasecausinggene/add/':
            add_gene_link = driver.find_element_by_css_selector('a[href="/admin/disease/diseasecausinggene/add/"].btn.btn-outline-success.float-right')
            add_gene_link.click()
            continue
        save_button = driver.find_element_by_name("_save")
        save_button.click()

        count = None
        try:    
            while driver.find_element_by_xpath('//div[@class="help-block text-red"]//li[text()="Gene with this Slug already exists."]'):
                if count is None:
                    count = 2
                    slug_name = driver.find_element_by_name('slug')
                    slug_name.clear()
                    slug_name.send_keys(f'{slug_to_be_sent}{count}')
                    save_button = driver.find_element_by_name("_save")
                    save_button.click()
                else:
                    count += 1
                    slug_name = driver.find_element_by_name('slug')
                    slug_name.clear()
                    slug_name.send_keys(f'{slug_to_be_sent}{count}')
                    save_button = driver.find_element_by_name("_save")
                    save_button.click()
        except:
            continue
        print(f'**** SUCCESSFULLY SUBMITTED {gene_name} ****')
        driver.close()
driver.quit()
print('*********** DONE SUCCESSFULLY ***********')
