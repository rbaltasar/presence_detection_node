#include <boost/interprocess/sync/scoped_lock.hpp>
#include <boost/interprocess/sync/named_mutex.hpp>
#include <fstream>
#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <stdio.h>
#include <thread>
#include <string>
#include <sys/types.h>
#include <unistd.h>


int main (int argc, const char *argv[])
{

  try
  {
    //Open or create the named mutex
    boost::interprocess::named_mutex mutex(boost::interprocess::open_or_create, "ble_node_mutex");

    //Lock named mutex
    boost::interprocess::scoped_lock<boost::interprocess::named_mutex> lock(mutex);

    std::string command = "sudo python /home/pi/Projects/presence_detection_node/presence_detection.py";

    //Execute python script: TTS and audio download
    system(command.c_str());

  }

  catch(boost::interprocess::interprocess_exception &ex){
      std::cout << ex.what() << std::endl;
      return 1;
   }

  return 0;
}
