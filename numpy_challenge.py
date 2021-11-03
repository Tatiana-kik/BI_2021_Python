import numpy as np


# Task #1:  Create 3 arrays.
def create_arrays():
    a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
    b = np.ones((3, 4))
    c = np.empty((3, 4))
    if 0:
        print(a)
        print(b)
        print(c)


# Task #2:  Multiply 2 matrices.
def matrix_multiplication(mat1, mat2):
    mat_res = np.dot(mat1, mat2)
    return mat_res


# Task #3:  Check multiplication
def multiplication_check(mat_list):
    try:
        mm = np.identity((mat_list[0].shape[0]))
        for m in mat_list:
            mm = np.dot(mm, m)
            # print(mm)
    except Exception:
        return False
    return True


# Task #4:  Multiply matrices.
def multiply_matrices(mat_list):
    mm = np.identity((mat_list[0].shape[0]))
    try:
        for m in mat_list:
            mm = np.dot(mm, m)
            # print(mm)
    except Exception:
        return None
    return mm


# Task #5:  Compute distance between 2 points in 2D coordinate system.
def compute_2d_distance(p1, p2):
    lx = p1[0] - p2[0]
    ly = p1[1] - p2[1]
    res = np.sqrt(lx**2 + ly**2)
    return res


# Task #6:  Compute distance between 2 points in xD coordinate system.
def compute_multidimensional_distance(p1, p2):
    diff = p1 - p2
    sqwr = diff ** 2
    res = np.sqrt(sqwr.sum())
    return res


# Task #7:  Compute pair distances.
def compute_pair_distances(mat):
    res = np.zeros((mat.shape[0], mat.shape[0]))
    for i in range(len(mat)-1):
        for j in range(i+1, len(mat)):
            # print(mat[i], mat[j])
            diff = mat[i] - mat[j]
            sqwr = diff ** 2
            dist = np.sqrt(sqwr.sum())
            res[i, j] = dist
            res[j, i] = dist
    return res


# Tests
if __name__ == "__main__":

    if 0:
        # test 2
        b = np.array([[7, 8], [9, 10], [11, 12]])
        # a = np.array([[1, 2, 3], [4, 5, 6]])
        a = np.identity((b.shape[0]))
        c = matrix_multiplication(a, b)
        print(a)
        print(b)
        print(c)

    if 0:
        # test 3
        # a = np.array([[1, 2, 3], [4, 5, 6]])
        b = np.array([[7, 8], [9, 10], [11, 12]])
        a = np.identity((b.shape[0]))
        c = np.array([[1], [2]])
        print(a)
        print(b)
        print(c)
        ok = multiplication_check([a, b, c])
        print(ok)

    if 0:
        # test 4
        b = np.array([[7, 8], [9, 10], [11, 12]])
        # a = np.array([[1, 2, 3], [4, 5, 6]])
        a = np.identity((b.shape[0]))
        c = np.array([[1], [2], [3], [4]])
        print(a)
        print(b)
        print(c)
        res = multiply_matrices([a, b, c])
        print(res)

    if 0:
        # test 5
        x = np.array([3, 3])
        y = np.array([2, 2])
        d = compute_2d_distance(x, y)
        print(d)

    if 0:
        # test 6
        x = np.array([1, 2, 3, 6])
        y = np.array([1, 2, 2, 6])
        d = compute_multidimensional_distance(x, y)
        print(d)

    if 0:
        # test 7
        mat_inc = np.array([[5, 5], [2, 3], [4, 5]])
        mat_dist = compute_pair_distances(mat_inc)
        print(mat_inc)
        print(mat_dist)
