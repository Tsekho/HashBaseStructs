import pytest
import random
from hashBaseStructs.structs.merkle_tree import MerkleTree

def data_generator(seed, length, max_number):
    random.seed(seed)
    data = []
    for i in range(length):
        item = random.randrange(-max_number, max_number)
        data.append((i, item))

    random.shuffle(data)
    return data


@pytest.fixture(scope="function", params=[
    (15, 10, 100),
    (25, 100, 1000)
])
def data_fixture(request):
    seed = request.param[0]
    length = request.param[1]
    max_number = request.param[2]
    data = data_generator(seed, length, max_number)
    return data

@pytest.fixture(scope="function")
def tree():
    return MerkleTree()

@pytest.fixture(scope="function", params=[
    (15, 10, 100),
    (25, 100, 1000)
])
def two_trees_with_data(request):
    tree_source = MerkleTree()
    tree_destination = MerkleTree()
    seed = request.param[0]
    length = request.param[1]
    max_number = request.param[2]
    data = data_generator(seed, length, max_number)
    
    for i in range(0, length):
        if i % 2 == 0:
            tree_source[data[i][0]] = data[i][1]
        else:
            tree_destination[data[i][0]] = data[i][1]

    return {"Source": tree_source, "Destination": tree_destination}

# Basic tests
def test_basic(tree):
    assert len(tree) == 0

# Test CRUD functionality
def test_set_get(tree, data_fixture):
    for item in data_fixture:
        tree[item[0]] = item[1]

    random.shuffle(data_fixture)

    for item in data_fixture:
        assert tree[item[0]] == item[1]
    
    assert len(tree) == len(data_fixture)

def test_add_range(tree, data_fixture):
    keys = []
    values = []
    
    for item in data_fixture:
        keys.append(item[0])
        values.append(item[1])
    
    tree.add_range(keys, values)

    random.shuffle(data_fixture)

    for item in data_fixture:
        assert tree[item[0]] == item[1]

    assert len(tree) == len(data_fixture)

def test_update(tree, data_fixture):
    keys = []
    values = []
    
    for item in data_fixture:
        keys.append(item[0])
        values.append(item[1])
    
    tree.add_range(keys, values)

    random.shuffle(values)

    for value, key in zip(values, keys):
        tree[key] = value
        assert len(tree) == len(data_fixture)
        assert tree[key] == value

def test_contain(tree, data_fixture):
    for item in data_fixture:
        tree[item[0]] = item[1]

    random.shuffle(data_fixture)

    for item in data_fixture:
        assert item[0] in tree

def test_delite(tree,  data_fixture):
    for item in data_fixture:
        tree[item[0]] = item[1]

    random.shuffle(data_fixture)

    for item in data_fixture:
        del tree[item[0]]
        assert not item[0] in tree
    
    assert len(tree) == 0

# Test methodth for CDC 
def test_eq(two_trees_with_data):
    tree_source = two_trees_with_data["Source"]
    tree_destination = two_trees_with_data["Destination"]

    assert tree_source == tree_source
    assert not tree_source == tree_destination

    assert not tree_source != tree_source
    assert tree_source!= tree_destination

def test_changeset():
    pass

# Test help methodth
def test_swap():
    pass

def test_clear(tree, data_fixture):
    for item in data_fixture:
        tree[item[0]] = item[1]

    tree.clear()

    assert len(tree) == 0

