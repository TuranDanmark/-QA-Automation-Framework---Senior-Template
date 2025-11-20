from ui.pages.alibaba_page import AlibabaPage

def test_alibaba_search(page):
    alibaba = AlibabaPage(page)
    alibaba.open()
    alibaba.search("apple")
    assert alibaba.results_loaded()
