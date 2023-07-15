#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    int sum = 0;
    int checksum = 0;
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    string key = argv[1];

    for (int j = 0, n = strlen(key); j < n; j++)
    {
        if (isalpha(key[j]) == false)
        {
            printf("key invalid\n");
            return 1;
        }
        for (int k = 0, m = strlen(key); k < m ; k++)
        {
            if(key[j] == key[k] && k != j)
            {
                printf("key invalid\n");
                return 1;
            }
        }

    }

    string s = get_string("plaintext: ");
    // for-loop for each letter in plaintext
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        // conversion lower-case
        if (s[i] >= 'a' && s[i] <= 'z')
        {
            if (key[s[i]- 97] >= 'a' && key[s[i]- 97] <= 'z') //key islower
            {
                s[i] = key[s[i] - 97];
            }
            else
            {
                s[i] = key[s[i] - 97] + 32;
            }
        }
        // conversion upper-case
        else if (s[i] >= 'A' && s[i] <= 'Z')
        {
            if (key[s[i]- 65] >= 'A' && key[s[i]- 65] <= 'Z') // key isupper
            {
                s[i] = key[s[i] - 65];
            }
            else
            {
                s[i] = (key[s[i] - 65]) - 32;
            }
        }


    }
    printf("ciphertext: %s\n", s);
}