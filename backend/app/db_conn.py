# from sqlite4 import SQLite4
import sqlite3


class DbConnection():
  def __init__(self) -> None:
    con = sqlite3.connect("hakatlopi.db")
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS RESULTS(prompt, answer, reference, correctness, correctness_exp, faithfulness, faithfulness_exp, guideline, guideline_exp, pairwise, pairwise_exp, relevancy, relevancy_exp, semantics, semantics_exp)")
    self.conn = con
    self.cur = cur

  def add_result(self, 
                 prompt, answer, 
                 reference, correctness, correctness_exp, 
                 faithfulness, faithfulnes_exp, guideline, guideline_exp, 
                 pairwise, pairwise_exp, relevancy, relevancy_exp, 
                 semantics, semantics_exp):    
    data = [
      (
        prompt, answer, reference, 
        correctness, correctness_exp, faithfulness, faithfulnes_exp, 
        guideline, guideline_exp, pairwise, pairwise_exp, 
        relevancy, relevancy_exp, semantics, semantics_exp
      )
    ]
    self.cur.executemany("INSERT INTO RESULTS VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    self.conn.commit()
    
  def retrieve_all(self):
    res = self.cur.execute("SELECT * FROM RESULTS")
    output = res.fetchall()
    return output