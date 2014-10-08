#ifndef DATAFETCHER_H_
#define DATAFETCHER_H_

#include <stdint.h>

#include <string>
#include <vector>

#include <TTree.h>

class DataFetcher {
 public:

  DataFetcher(std::string file_path);
  ~DataFetcher();

  //int * event_number();

  void get_entry(unsigned int entry);

  unsigned int entries() {
    return entries_;
  }

  // TODO: Rename to adc_number_wires()?
  unsigned int adc_rows() {
    return adc_rows_;
  }

  // TODO: Rename to adc_number_time_ticks() or adc_number_samples()?
  unsigned int adc_cols() {
    return adc_cols_;
  }

  short * adc() {
    short * adc_array = &adc_[0];
    return adc_array;
  }

  uint32_t * channel() {
    uint32_t * channel_array = &channel_[0];
    return channel_array;
  }

  double * pedestal() {
    double * pedestal_array = &pedestal_[0];
    return pedestal_array;
  }

  unsigned int number_particles() {
    return number_particles_;
  }

  int * pdg_code() {
    int * pdg_code_array = &pdg_code_[0];
    return pdg_code_array;
  }

  int * track_id() {
    int * track_id_array = &track_id_[0];
    return track_id_array;
  }

  int * parent_id() {
    int * parent_id_array = &parent_id_[0];
    return parent_id_array;
  }

  double * start_momentum() {
    double * start_momentum_array = &start_momentum_[0];
    return start_momentum_array;
  }

  double * trajectory_length() {
    double * trajectory_length_array = &trajectory_length_[0];
    return trajectory_length_array;
  }

  std::vector<std::string> process() {
    return process_;
  }

  std::vector< std::vector<double> > particle_x() {
    return particle_x_;
  }
  std::vector< std::vector<double> > particle_y() {
    return particle_y_;
  }
  std::vector< std::vector<double> > particle_z() {
    return particle_z_;
  }
  std::vector< std::vector<double> > particle_t() {
    return particle_t_;
  }
  std::vector< std::vector<double> > particle_px() {
    return particle_px_;
  }
  std::vector< std::vector<double> > particle_py() {
    return particle_py_;
  }
  std::vector< std::vector<double> > particle_pz() {
    return particle_pz_;
  }
  std::vector< std::vector<double> > particle_energy() {
    return particle_energy_;
  }

 private:

  std::string file_path_;
  TTree * tree_;

  std::vector<std::string> FindLeavesOfType(std::string pattern);

  unsigned int entries_;
  unsigned int adc_rows_;
  unsigned int adc_cols_;
  unsigned int number_particles_;

  std::vector<short> adc_;
  std::vector<uint32_t> channel_;
  std::vector<double> pedestal_;
  std::vector<int> pdg_code_;
  std::vector<int> track_id_;
  std::vector<int> parent_id_;
  std::vector<std::string> process_;
  std::vector<double> start_momentum_;
  std::vector<double> trajectory_length_;
  std::vector< std::vector<double> > particle_x_;
  std::vector< std::vector<double> > particle_y_;
  std::vector< std::vector<double> > particle_z_;
  std::vector< std::vector<double> > particle_t_;
  std::vector< std::vector<double> > particle_px_;
  std::vector< std::vector<double> > particle_py_;
  std::vector< std::vector<double> > particle_pz_;
  std::vector< std::vector<double> > particle_energy_;

};

#endif  // DATAFETCHER_H_
