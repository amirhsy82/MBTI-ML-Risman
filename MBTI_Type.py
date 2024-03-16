from MBTI_app import Message

def Type():
    messages = Message.query.order_by(Message.id).all()

    type_dict = {}
    for message in messages:
        if message.mbti_type not in type_dict.keys():
            type_dict.__setitem__(message.mbti_type, 1)
        else:
            type_dict[message.mbti_type] += 1

    type_dict = dict(sorted(type_dict.items(), key=lambda x:x[1], reverse=True))
    res = dict(list(type_dict.items())[:2]) 

    counter = 0
    for key in type_dict:
        counter += type_dict[key]

    List = []
    for key in type_dict:
        List.append(f"You are {type_dict[key]/3 * 100 :.2f}% {key}")
        
    return List