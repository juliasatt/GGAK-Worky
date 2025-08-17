/**********************************************************************
 * This file is used for testing random stuff without running the
 * whole of SatDump, which comes in handy for debugging individual
 * elements before putting them all together in modules...
 *
 * If you are an user, ignore this file which will not be built by
 * default, and if you're a developper in need of doing stuff here...
 * Go ahead!
 *
 * Don't judge the code you might see in there! :)
 **********************************************************************/

#include "init.h"
#include "logger.h"

#include <cstdint>
#include <cstdio>
#include <cstring>
#include <fstream>

int main(int argc, char *argv[])
{
    initLogger();

    logger->set_level(slog::LOG_OFF);
    satdump::initSatdump();
    completeLoggerInit();
    logger->set_level(slog::LOG_TRACE);

    uint8_t frms[448];
    uint8_t frm[224];

    std::ifstream data_in(argv[1]);

    std::ofstream out_0("out_0.bin");
    std::ofstream out_1("out_1.bin");
    std::ofstream out_2("out_2.bin");
    std::ofstream out_3("out_3.bin");
    std::ofstream out_4("out_4.bin");
    std::ofstream out_5("out_5.bin");
    std::ofstream out_6("out_6.bin");
    std::ofstream out_7("out_7.bin");
    // std::ofstream data_ou(argv[2]);

    // std::vector<uint8_t> full_payload;

    while (!data_in.eof())
    {
        data_in.read((char *)frms, 448);

        memset(frm, 0, 224);
        memcpy(frm, frms, 224);

        int marker = frm[4] >> 4;

        if (marker == 0)
            out_0.write((char *)frm, 224);
        else if (marker == 1)
            out_1.write((char *)frm, 224);
        else if (marker == 2)
            out_2.write((char *)frm, 224);
        else if (marker == 3)
            out_3.write((char *)frm, 224);
        else if (marker == 4)
            out_4.write((char *)frm, 224);
        else if (marker == 5)
            out_5.write((char *)frm, 224);
        else if (marker == 6)
            out_6.write((char *)frm, 224);
        else if (marker == 7)
            out_7.write((char *)frm, 224);

        // printf("%d\n", marker);
        // logger->trace(marker);
        // data_ou.write((char *)frm, 224);
    }
}
