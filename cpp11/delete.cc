#include <iostream>
using namespace std;

class parent
{
public:
    int x;
};

class child : public parent
{
public:
    int x;
    child() = default;
    child(const child &) = delete;
};
int main()
{
    child c;
    child c1(c); // error because copy constructor is deleted
    return 0;
}