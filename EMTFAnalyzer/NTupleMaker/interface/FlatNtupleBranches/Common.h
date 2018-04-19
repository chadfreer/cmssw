
#ifndef FlatNtupleBranchesCommon_h
#define FlatNtupleBranchesCommon_h

#include <iostream>
#include <vector>
#include <map>
#include "TString.h"

// Default values for maps
const int       DINT  = -999;
const float     DFLT  = -999.;
const long long DLONG = -999;
const std::vector<float> DVFLT;
const std::vector<int>   DVINT;
const std::vector<std::vector<int> > DVVINT;



///////////////////////////////////////////////////////////////////////
///  Assign values to elements of std::map with debugging included  ///
///////////////////////////////////////////////////////////////////////

inline void INSERT(std::map<TString, int> & iMap, const TString iStr, const int iInt) {
  try { iMap.at(iStr) = iInt; }
  catch (const std::exception& e) { std::cout << "\n\nINSERT: No matching 'int' element found for string: '" << iStr << "' - code will break\n\n" << std::endl;
    iMap.at(iStr) = iInt; }
};
inline void INSERT(std::map<TString, long long> & iMap, const TString iStr, const long long iLong) {
  try { iMap.at(iStr) = iLong; }
  catch (const std::exception& e) { std::cout << "\n\nINSERT: No matching 'long long' element found for string: '" << iStr << "' - code will break\n\n" << std::endl;
    iMap.at(iStr) = iLong; }
};
inline void INSERT(std::map<TString, std::vector<float> > & iMap, const TString iStr, const float iFlt) {
  try { iMap.at(iStr).push_back(iFlt); }
  catch (const std::exception& e) { std::cout << "\n\nINSERT: No matching 'std::vector<float>' element found for string: '" << iStr << "' - code will break\n\n" << std::endl;
    iMap.at(iStr).push_back(iFlt); }
};
inline void INSERT(std::map<TString, std::vector<float> > & iMap, const TString iStr, const int idx, const float iFlt) {
  try { iMap.at(iStr).at(idx) = iFlt; }
  catch (const std::exception& e) { std::cout << "\n\nINSERT: No matching 'float' element found for string: '" << iStr << "' at index " << idx << " - code will break\n\n" << std::endl;
    iMap.at(iStr).push_back(iFlt); }
};
inline void INSERT(std::map<TString, std::vector<int> > & iMap, const TString iStr, const int iInt) {
  try { iMap.at(iStr).push_back(iInt); }
  catch (const std::exception& e) { std::cout << "\n\nINSERT: No matching 'std::vector<int>' element found for string: '" << iStr << "' - code will break\n\n" << std::endl;
    iMap.at(iStr).push_back(iInt); }
};
inline void INSERT(std::map<TString, std::vector<int> > & iMap, const TString iStr, const int idx, const int iInt) {
  try { iMap.at(iStr).at(idx) = iInt; }
  catch (const std::exception& e) { std::cout << "\n\nINSERT: No matching 'int' element found for string: '" << iStr << "' at index " << idx << " - code will break\n\n" << std::endl;
    iMap.at(iStr).push_back(iInt); }
};
inline void INSERT(std::map<TString, std::vector<std::vector<int> > > & iMap, const TString iStr, const std::vector<int> iVInt) {
  try { iMap.at(iStr).push_back(iVInt); }
  catch (const std::exception& e) { std::cout << "\n\nINSERT: No matching 'std::vector<std::vector<int>>' element found for string: '" << iStr << "' - code will break\n\n" << std::endl;
    iMap.at(iStr).push_back(iVInt); }
};
inline void INSERT(std::map<TString, std::vector<std::vector<int> > > & iMap, const TString iStr, const int iInt) {
  try { iMap.at(iStr).back().push_back(iInt); }
  catch (const std::exception& e) { std::cout << "\n\nINSERT: No matching 'std::vector<std::vector<int>>' element found for string: '" << iStr << "' - code will break\n\n" << std::endl;
    iMap.at(iStr).back().push_back(iInt); }
};


/////////////////////////////////////////////////////////////////////////
///  Access values from elements of std::map with debugging included  ///
/////////////////////////////////////////////////////////////////////////

inline int ACCESS(const std::map<TString, int> & iMap, const TString iStr) {
  try { return iMap.at(iStr); }
  catch (const std::exception& e) { std::cout << "\n\nACCESS: No matching 'int' element found for string: '" << iStr << "' - code will break\n\n" << std::endl;
    return iMap.at(iStr); }
};
inline long long ACCESS(const std::map<TString, long long> & iMap, const TString iStr) {
  try { return iMap.at(iStr); }
  catch (const std::exception& e) { std::cout << "\n\nACCESS: No matching 'long long' element found for string: '" << iStr << "' - code will break\n\n" << std::endl;
    return iMap.at(iStr); }
};
inline std::vector<float> ACCESS(const std::map<TString, std::vector<float> > & iMap, const TString iStr) {
  try { return iMap.at(iStr); }
  catch (const std::exception& e) { std::cout << "\n\nACCESS: No matching 'std::vector<float>' element found for string: '" << iStr << "' - code will break\n\n" << std::endl;
    return iMap.at(iStr); }
};
inline std::vector<int> ACCESS(const std::map<TString, std::vector<int> > & iMap, const TString iStr) {
  try { return iMap.at(iStr); }
  catch (const std::exception& e) { std::cout << "\n\nACCESS: No matching 'std::vector<int>' element found for string: '" << iStr << "' - code will break\n\n" << std::endl;
    return iMap.at(iStr); }
};
inline std::vector<std::vector<int> > ACCESS(const std::map<TString, std::vector<std::vector<int> > > & iMap, const TString iStr) {
  try { return iMap.at(iStr); }
  catch (const std::exception& e) { std::cout << "\n\nACCESS: No matching 'std::vector<std::vector<int>>' element found for string: '" << iStr << "' - code will break\n\n" << std::endl;
    return iMap.at(iStr); }
};

#endif  // #ifndef FlatNtupleBranchesCommon_h
