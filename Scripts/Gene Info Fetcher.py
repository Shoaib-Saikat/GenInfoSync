from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

file_name = input('Do not put the extension!!! Enter filename: ')

fh = open(f'{file_name}.txt', 'r')

fw = open(f'COMPLETED_{file_name}.txt', 'w')

PATH = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(PATH)

count = 1

for gene_details in fh:
    if gene_details.startswith('GeneID'):
        fw.write('gene_id\tgene_name\tprotein_name\tchromosomal_location\tnucleotide_accession\tmode_of_inheritance\tgenecard_link\tkegg_link,pdb_link\tentrez_link\tomim_link')
        fw.write('\n')
        continue
    else:
        temp_list = []
        gene_details_list = gene_details.split('\t')
        gene_name = gene_details_list[1]
        print(f'->>>>>>>>> Seaching gene {gene_name} Serial: {count}')
        omim= gene_details_list[7].strip()
        temp_list.append(gene_details_list[0])
        temp_list.append(gene_name)
        temp_list.append(gene_details_list[2].replace('"',''))

        try:
            chromosomal_location = f'Chromosome {gene_details_list[3]}, {gene_details_list[4]} ({gene_details_list[5]}..{gene_details_list[6]})'
            temp_list.append(chromosomal_location)
        except:
            temp_list.append('')

        if not len(omim)<1:
            omim_link = f'https://www.omim.org/entry/{omim}'
            temp_list.append(omim_link)
        else:
            temp_list.append('')
        genecard_link = f'https://www.genecards.org/cgi-bin/carddisp.pl?gene={gene_name}'
        temp_list.append(genecard_link)

        entrez_link = f'https://www.ncbi.nlm.nih.gov/search/all/?term={gene_name}'
        temp_list.append(entrez_link)

        url_genecard = f'https://www.genecards.org/cgi-bin/carddisp.pl?gene={gene_name}'
        driver.get(url_genecard)

        mode_of_inheritance_list = []

        paragraphs = driver.find_elements_by_tag_name('td')
        for p in paragraphs:
            text_data = p.text
            if "Autosomal dominant inheritance" in text_data:
                mode_of_inheritance_list.append("Autosomal dominant inheritance")
                break

        for p in paragraphs:
            text_data = p.text
            if "Autosomal recessive inheritance" in text_data:
                mode_of_inheritance_list.append("Autosomal recessive inheritance")
                break

        mode_of_inheritance = ', '.join(mode_of_inheritance_list)
        temp_list.append(mode_of_inheritance)

        try:
            url_kegg = 'https://www.genome.jp/kegg/'
            driver.get(url_kegg)

            search_kegg = driver.find_element_by_name('text')
            search_kegg.send_keys(gene_name)

            search_button_kegg = driver.find_element_by_xpath("//input[@type='button' and @value='Search']")
            search_button_kegg.click()

            anchor_element_kegg = driver.find_element_by_xpath("//a[starts-with(@href, '/entry/')]")
            anchor_element_kegg.click()

            current_url_kegg = driver.current_url
            temp_list.append(current_url_kegg)
        except:
            temp_list.append('')
            


        try:
            url_nuc_accession = f'https://www.ncbi.nlm.nih.gov/nuccore/?LinkName=gene_nuccore_refseqgene&from_uid={gene_details_list[0]}'
            driver.get(url_nuc_accession)
            locus = driver.find_element(By.CLASS_NAME, "itemid").text
            accession_nuc_start_ndx = locus.find(':')
            nucleotide_accession = locus[accession_nuc_start_ndx+2:]
            temp_list.append(nucleotide_accession)
        except:
            temp_list.append('')

        url_rcsb = 'https://www.rcsb.org/search?request=%7B%22query%22%3A%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22terminal%22%2C%22service%22%3A%22full_text%22%2C%22parameters%22%3A%7B%22value%22%3A%22tumor%20necrosis%20factor%22%7D%7D%5D%2C%22logical_operator%22%3A%22and%22%7D%5D%2C%22logical_operator%22%3A%22and%22%2C%22label%22%3A%22full_text%22%7D%2C%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22terminal%22%2C%22service%22%3A%22text%22%2C%22parameters%22%3A%7B%22attribute%22%3A%22rcsb_entity_source_organism.ncbi_scientific_name%22%2C%22value%22%3A%22Homo%20sapiens%22%2C%22operator%22%3A%22exact_match%22%7D%7D%5D%2C%22logical_operator%22%3A%22or%22%2C%22label%22%3A%22rcsb_entity_source_organism.ncbi_scientific_name%22%7D%5D%2C%22logical_operator%22%3A%22and%22%7D%5D%2C%22logical_operator%22%3A%22and%22%2C%22label%22%3A%22text%22%7D%5D%2C%22logical_operator%22%3A%22and%22%7D%2C%22return_type%22%3A%22entry%22%2C%22request_options%22%3A%7B%22paginate%22%3A%7B%22start%22%3A0%2C%22rows%22%3A25%7D%2C%22results_content_type%22%3A%5B%22experimental%22%5D%2C%22sort%22%3A%5B%7B%22sort_by%22%3A%22score%22%2C%22direction%22%3A%22desc%22%7D%5D%2C%22scoring_strategy%22%3A%22combined%22%7D%2C%22request_info%22%3A%7B%22query_id%22%3A%226e21a235eac75896d5a5a51222df8c5c%22%7D%7D'
        driver.get(url_rcsb)

        full_text_box = driver.find_element_by_css_selector("input[placeholder='Enter one or more search terms.']")
        full_text_box.clear()


        string = gene_details_list[2].replace('"','')
        full_text_box.send_keys(string)

        search_button_rcsb = driver.find_element_by_css_selector("div[style*='background-color: rgb(50, 88, 128)'] span[data-cy='searchButton']")
        search_button_rcsb.click()

        current_url_pdb = driver.current_url

        shorten_url = "https://url-shortener23.p.rapidapi.com/shorten"
        alias = ""

        payload = "{\"url\":\"" + current_url_pdb + "\",\"alias\":\"" + alias + "\"}"
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "ce78ea6c84msh1b089ff702b2d7fp15bf32jsne562438810e3",
            "X-RapidAPI-Host": "url-shortener23.p.rapidapi.com"
        }
        try:
            response = requests.request("POST", shorten_url, data=payload, headers=headers)
            pdb_link_short = response.json()['short_url']
            temp_list.append(pdb_link_short)
        except:
            response = requests.request("POST", shorten_url, data=payload, headers=headers)
            pdb_link_short = response.json()
            print('-------Result_url not found>>>>>',pdb_link_short)

        fw.write(f'{temp_list[0]}\t{gene_name}\t{temp_list[2]}\t{temp_list[3]}\t{temp_list[9]}\t{temp_list[7]}\t{temp_list[5]}\t{temp_list[8]}\t{temp_list[10]}\t{temp_list[6]}\t{temp_list[4]}')
        fw.write('\n')
        print('*******************************************')
        print(temp_list)
        count+=1
        print('*******************************************')

fh.close()
fw.close()
driver.quit()
