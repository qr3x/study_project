void fillDepth(int tree[], int i, int depth[])
{
    // climb up the tree until we find -1
    // as we find, we start looking for children -1 and etc

    int number = tree[i];
    if (number == -1)
    {
        depth[i] = 1;

        return;
    }

    if (depth[number] == 0)
        fillDepth(tree, number, depth);

    depth[i] = depth[number] + 1;
}

int findHeight(int tree[], int len)
{
    int* depth = new int[len];
    for (int i = 0; i < len; i++)
        depth[i] = 0;

    // find all the depths
    for (int i = 0; i < len; i++)
        fillDepth(tree, i, depth);

    // find the height of the tree (maximum of the depths)
    int heightTree = depth[0];
    for (int i = 0; i < len; i++)
        if (heightTree < depth[i])
            heightTree = depth[i];

    return heightTree;
}