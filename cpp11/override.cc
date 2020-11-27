#include <iostream>

using namespace std;

class parent
{
public:
    int x;
    // virtual void func()
    // {
    //     cout << "parent" << endl;
    // }
};

class child : public parent
{
public:
    int x;
    void func() override
    {
        cout << "child" << endl;
    }
};

int main()
{
    child c;
    c.func();
    return 0;
}