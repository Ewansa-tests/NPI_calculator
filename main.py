from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
#task 3
import sqlite3

#task 4
from fastapi.responses import StreamingResponse
import csv,io

DBCALC = 'calculator.db'
#instance of API
app = FastAPI()

def init_db():
    connection=sqlite3.connect(DBCALC)
    curr = connection.cursor()
    curr.execute('''
        CREATE TABLE IF NOT EXISTS calculator(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   expression TEXT NOT NULL,
                   result INTEGER NOT NULL
        )
    ''')
    connection.commit()
    connection.close()

init_db()


class Expression(BaseModel):
    expression: str

def calculate_api(expression: str) -> int:  #modified after pytests
    expression=expression.split()

    # create stack
    s = []

    for element in expression:
        if element not in '*/+-':
            try:
                s.append(int(element))
            except ValueError:
                raise ValueError("Invalid token in expression")
        else:
            if len(s) < 2:
                raise ValueError("Invalid RPN expression")
            right = s.pop()
            left = s.pop()
            if element == '+':
                s.append(left + right)
            elif element == '-':
                s.append(left - right)
            elif element == '*':
                s.append(left * right)
            elif element == '/':
                if right == 0:
                    raise ZeroDivisionError("division by zero")
                s.append(int(left / right))

    if len(s) != 1:
        raise ValueError("Invalid RPN expression")

    return s.pop()

#Save to DB

#task 3
def save_record(expression: str, result: int):
    connection = sqlite3.connect(DBCALC)
    curr = connection.cursor()
    curr.execute('''
        INSERT INTO calculator(expression, result) VALUES(?,?)''',
        (expression, result))
    connection.commit()
    connection.close()


# task 4
def collect_records():
    connection = sqlite3.connect(DBCALC)
    curr = connection.cursor()
    curr.execute('Select * FROM calculator')
    records = curr.fetchall()
    connection.close()
    return records


@app.post("/calculate")
async def calculate(expression:Expression):
    try:
        result = calculate_api(expression.expression)
        save_record(expression.expression, result)
        return {"result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/recup")
async def export():
    records = collect_records()

    #create a csv file 
    output=io.StringIO()
    writer=csv.writer(output)
    writer.writerow(['ID','Expression','Result'])
    writer.writerows(records)
    output.seek(0)

    response= StreamingResponse(output,media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=calculator_records.csv"
    return response