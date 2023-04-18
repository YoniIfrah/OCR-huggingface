from OCR import fix_date

def test_fix_date():
    fix_date('1787')
    fix_date('0787')
    fix_date('1707')
    fix_date('0707')
    fix_date('1010')