/* -*-mode:c++; tab-width: 2; indent-tabs-mode: nil; c-basic-offset: 2 -*- */

#ifndef PATHS_HH
#define PATHS_HH

#include <string>
#include <stdexcept>
#include <vector>
#include <sys/types.h>

#include "path.hh"
#include "optional.hh"

namespace gg {
  namespace paths {
    roost::path blobs();
    roost::path reductions();

    roost::path blob_path( const std::string & hash );
    roost::path reduction_path( const std::string & hash );
  }

  namespace cache {
    struct ReductionResult
    {
      std::string hash;
      size_t order;
      /* XXX add this: off_t size; */
    };

    Optional<ReductionResult> check( const std::string & thunk_hash );
    void insert( const std::string & old_hash, const std::string & new_hash );
  }

  namespace models {
    std::vector<std::string> args_to_vector( int argc, char ** argv );
  }
}

#endif /* PATHS_HH */