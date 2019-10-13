def chunkify(userlist, chunkSize=200):
    chunks = [[]]
    count = 0
    m = 0
    for list1 in userlist:
        if count < chunkSize:
            chunk = chunks[-1]
            count = count + 1
        else:
            chunks.append([])
            chunk = chunks[-1]
            count = 1
        chunk.append(list1)
    print(chunks)

chunkify(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'], 5)