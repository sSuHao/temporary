#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Check command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // Open the file in read mode
    FILE *infile = fopen(argv[1], "r");
    if (infile == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Read the files and store in buffer
    BYTE *buffer = malloc (sizeof(BYTE) * 512);
    while(fread(buffer, sizeof(BYTE), 512, infile) == 512)
    {
    // Check if it's the start of new JPEG
    if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
    {
        char *namefile = malloc(sizeof(char) * 8);
        char *s = malloc(sizeof(char) * 8);
        sprintf(namefile, "%03i.jpg", i);
        FILE *outfile = fopen(namefile, "w");
        fwrite(buffer, sizeof(BYTE), 512, outfile);
        free(s);
        free(namefile);
    }
    }
    free(buffer);
    fclose(infile);
}
