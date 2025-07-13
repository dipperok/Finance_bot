def is_db_test_print(db_mane):
    if "test" in db_mane.lower():
        print('БОТ ЗАПУЩЕН НА ТЕСТОВОЙ БД!')
        return True
    else:
        return False
    
    
if __name__ == "__main__":
    pass