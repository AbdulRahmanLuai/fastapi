def test_get_posts(authorized_client, test_posts):
    res = authorized_client.get('/posts')
    assert res.status_code == 200
    print(res.json())
    
    
    
    