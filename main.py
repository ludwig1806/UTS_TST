import json
from fastapi import FastAPI,HTTPException, Body, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from model import UserLoginSchema, UserSchema
from auth_bearer import JWTBearer
from auth_handler import signJWT

with open("menu.json", "r") as read_file:
    data = json.load(read_file)

with open("user.json", "r") as read_file:
    data_login = json.load(read_file)
app = FastAPI()
users = []

@app.get('/', tags=["root"])
def root() :
    return {"Welcome to my server"}
    
@app.get('/menu/',tags =["get"])
async def read_all_menu():
    return data

@app.get('/menu/{item_id}', tags=['get'])
async def read_menu(item_id: int):
    for menu_item in data['menu']:
        if menu_item['id'] ==item_id:
            return menu_item
    raise HTTPException(
        status_code =404, detail=f'"Item not found'
    )

@app.post('/menu', tags=['post'])
async def post_menu(name:str):
    id = 1
    if (len(data['menu'])>0) :
        id=data['menu'][len(data['menu'])-1]['id']+1
    new_data ={'id':id, 'name':name}
    data['menu'].append(dict(new_data))
    read_file.close()
    with open("menu.json", "w") as write_file:
        json.dump(data,write_file,indent=4)
    write_file.close()

    return (new_data)

    raise HTTPEXCEPTION(
        status_code=500, detail=f'Internal server error'
    )

@app.put('/menu/{item_id}', tags=['put'])
async def update_menu(item_id: int, name: str):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            menu_item['name'] = name
            read_file.close()
            with open("menu.json", "w") as write_file:
                json.dump(data,write_file,indent=4)
            write_file.close()
            
            return{"message":"Data updated"}
    raise HTTPException(
        status_code =404, detail=f'"Item not found'
    )

    
@app.delete('/menu/{item_id}',dependencies=[Depends(JWTBearer())], tags=['delete'])
async def delete_menu(item_id: int):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            data['menu'].remove(menu_item)
            read_file.close()
            with open("menu.json", "w") as write_file:
                json.dump(data,write_file,indent=4)
            write_file.close()
            
            return{"message":"Data deleted"}
    raise HTTPException(
        status_code =404, detail=f'"Item not found'
    )

@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    users.append(user)
    return signJWT(user.email)

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }
