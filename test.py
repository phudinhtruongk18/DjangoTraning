i = [2]

dict_1= {
    'a':1
}

categorys = [
    {
        'category':{

        }
    },
    {
        'category':{
            
        }
    },
    {
        'category':{
            
        }
    }
]

print(len(i))
print(len(dict_1))
temp_categorys = []
for category in categorys:
    temp_categorys =  Category(**category['category'])


Category.objects.bulk_create(temp_categorys)


