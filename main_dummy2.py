from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

#instance of API
app = FastAPI()

class Expression(BaseModel):
    expression: str

def calculate_api (expression:str)->int:
    # we assume that the expression is correctly formated so we seperate on spaces
    expression=expression.split()

    #create stack
    s=[]

    for element in expression:
        if element not in '*/+-':
            s.append(int(element))

        else:
            right = s.pop()
            left=s.pop()
            if element=='+':
                s.append(left+right)
            elif element=='-':
                s.append(left-right)
            elif element=='*':
                s.append(left*right)
            elif element=='/':
                s.append(int(left/right))
    
    return s.pop()

@app.post("/calculate")
async def calculate(expression:Expression):
    try:
        result = calculate_api(expression.expression)
        return {"result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


