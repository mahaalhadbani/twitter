import nest_asyncio 
nest_asyncio.apply()
import twint
import pandas as pd
import os
def test_reg(c, run):
    print("[+] Beginning vanilla test in {}".format(str(run)))
    run(c)


def test_db(c, run):
    print("[+] Beginning DB test in {}".format(str(run)))
    c.Database = "test_twint.db"
    run(c)


def custom(c, run, _type):
    print("[+] Beginning custom {} test in {}".format(_type, str(run)))
    c.Custom['tweet'] = ["id", "username"]
    c.Custom['user'] = ["id", "username"]
    run(c)


def test_json(c, run):
    c.Store_json = True
    c.Output = "test_twint.json"
    custom(c, run, "JSON")
    print("[+] Beginning JSON test in {}".format(str(run)))
    run(c)


def test_csv(c, run):
    c.Store_csv = True
    c.Output = "test_twint.csv"
    custom(c, run, "CSV")
    print("[+] Beginning CSV test in {}".format(str(run)))
    run(c)


def main():
   
    import nest_asyncio 
    nest_asyncio.apply()
    import twint
    import os
    f = twint.Config()
    f.Search ="khled hospitals"
    f.Store_json= True
    f.Limit = 5
    f.Pandas = True
    f.Output ="test_twint4.json"
    twint.run.Search(f)
    import pandas as pd
    pd.options.display.max_columns=50
    data=pd.read_json("test_twint4.json",lines=True)
    data.shape
    data.head()

if __name__ == '__main__':
    main()