#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int h = 0;
    int x = 1;
    int check = 1;
    int y = 1;
    do
    {
        h = get_int("Height: ");
    }
    while (h < 1 || h > 8);

    for (x = 0; x < h ; ++x)
    {
        for (int i = 1; i < h - x; i++)
        {
            printf(" ");
        }
        for (int j = 0; j <= x; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}