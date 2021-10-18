import json
from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

with open("menu.json", "r") as read_file:
    data = json.load(read_file)

with open("user.json", "r") as read_file:
    data_login = json.load(read_file)
app = FastAPI()

@app.get('/', tags=["root"])
def root() :
    return {"Menu" : "Item"}
    
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

    
@app.delete('/menu/{item_id}', tags=['delete'])
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

@app.get('/user/',tags =["get"])
async def read_all_user():
    return data_login

@app.post('/user', tags=['post'])
async def post_menu(username:str, password: str):
    id = 1
    if (len(data_login['user'])>0) :
        id=data['user'][len(data_login['user'])-1]['id']+1
    new_data ={'id':id, 'username':username, "password": password}
    data['user'].append(dict(new_data))
    read_file.close()
    with open("user.json", "w") as write_file:
        json.dump(data,write_file,indent=4)
    write_file.close()

    return (new_data)

    raise HTTPEXCEPTION(
        status_code=500, detail=f'Internal server error'
    )