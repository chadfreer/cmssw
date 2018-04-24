
import math

def HitsMatch( Hit1, Hit2 ):

	if ( Hit1.BX() == Hit2.BX() and Hit1.Station() == Hit2.Station() and Hit1.Sector() == Hit2.Sector() and
	     Hit1.Subsector() == Hit2.Subsector() and Hit1.Ring() == Hit2.Ring() and Hit1.Chamber() == Hit2.Chamber() and
	     Hit1.CSC_ID() == Hit2.CSC_ID() and Hit1.Strip() == Hit2.Strip() and Hit1.Wire() == Hit2.Wire() ):
		return True
	else:
		return False

def HitsMatchNoBX( Hit1, Hit2 ):

	if ( Hit1.Station() == Hit2.Station() and Hit1.Sector() == Hit2.Sector() and
	     Hit1.Subsector() == Hit2.Subsector() and Hit1.Ring() == Hit2.Ring() and Hit1.Chamber() == Hit2.Chamber() and
	     Hit1.CSC_ID() == Hit2.CSC_ID() and Hit1.Strip() == Hit2.Strip() and Hit1.Wire() == Hit2.Wire() and
	     Hit1.Quality() == Hit1.Quality() and Hit1.Bend() == Hit2.Bend() and Hit1.Pattern() == Hit2.Pattern() ):
		return True
	else:
		return False

def HitsMatchChamber( Hit1, Hit2 ):

	if ( Hit1.BX() == Hit2.BX() and Hit1.Endcap() == Hit2.Endcap() and Hit1.Station() == Hit2.Station() and 
	     Hit1.Sector() == Hit2.Sector() and Hit1.Subsector() == Hit2.Subsector() and Hit1.Ring() == Hit2.Ring() and 
	     Hit1.Chamber() == Hit2.Chamber() and Hit1.CSC_ID() == Hit2.CSC_ID() ):
		return True
	else:
		return False

## Only works for non-neighbor hits: need sector index for neighbor hits
def CalcPhiGlobDeg( phi_loc_int, sector ):
	
	phi_loc_deg = ( phi_loc_int / 60.0 ) - 22
	phi_glob_deg = phi_loc_deg + 60 * (sector - 1) + 15

	if (phi_glob_deg <   0): phi_glob_deg = phi_glob_deg + 360
	if (phi_glob_deg > 360): phi_glob_deg = phi_glob_deg - 360
	return phi_glob_deg

def CalcDPhi( phi1, phi2 ):
	dPhi = math.acos( math.cos( phi1 - phi2 ) )
	if math.sin( phi1 - phi2 ) < 0: dPhi *= -1
	return dPhi

def CalcDR( eta1, phi1, eta2, phi2 ):
	return math.sqrt( math.pow(CalcDPhi(phi1, phi2), 2) + math.pow(eta1 - eta2, 2) )
	

def HitPhiInChamber( Hit ):

	phi_glob_deg = Hit.Phi_glob_deg()
	if (phi_glob_deg <   0): phi_glob_deg = phi_glob_deg + 360
	if (phi_glob_deg > 360): phi_glob_deg = phi_glob_deg - 360

	# phi_loc_deg_corr = (Hit.Phi_loc_int() / (0.625 * 60)) * 0.97975745
	# phi_GMT = math.floor(phi_loc_deg_corr - 35)
	# phi_loc_deg = (phi_GMT * 0.625) + 0.3125
	# phi_glob_deg = phi_loc_deg + 60 * (Hit.Sector() - 1) + 15
	# if (phi_glob_deg > 180): phi_glob_deg = 360 - phi_glob_deg

	if ( Hit.Station() != 1 and Hit.Ring() == 1 ):
		chamber_center = 20.0 * (Hit.Chamber() - 1) + 5.0
		chamber_half_width = 10 + 5 ## 1.5
	else:
		chamber_center = 10.0 * (Hit.Chamber() - 1)
		chamber_half_width = 5 + 2.5 ## 0.75
	if (chamber_center <   0): chamber_center = chamber_center + 360
	if (chamber_center > 360): chamber_center = chamber_center - 360

	pi = 3.14159265358979323846
	return math.asin( math.sin( (phi_glob_deg - chamber_center)*(pi/180) ) ) * (180/pi)
		
	# if phi_glob_deg > 90 or phi_glob_deg < 270:
		# if abs(phi_glob_deg - chamber_center) > chamber_half_width:
		# 	print 'Hit in station %d, sector %d, ring %d, chamber %d has phi %.2f' % ( Hit.Station(), Hit.Sector(), Hit.Ring(),
		# 										   Hit.Chamber(), phi_glob_deg )
		# 	print 'Epected chamber range is %.2f to %.2f' % ( chamber_center - chamber_half_width, 
		# 							  chamber_center + chamber_half_width )
		# else:
		# 	print 'Hit in station %d, sector %d, ring %d, chamber %d OK!' % ( Hit.Station(), Hit.Sector(), Hit.Ring(), Hit.Chamber() )
		# return phi_glob_deg - chamber_center

	# else:
		# if phi_glob_deg > 180:
			# phi_glob_deg = phi_glob_deg - 360
		# if chamber_center > 180:
			# chamber_center = chamber_center - 360
		# if abs(phi_glob_deg - chamber_center) > chamber_half_width:
		# 	print 'Hit in station %d, sector %d, ring %d, chamber %d has phi %.2f' % ( Hit.Station(), Hit.Sector(), Hit.Ring(),
		# 										   Hit.Chamber(), phi_glob_deg )
		# 	print 'Epected chamber range is %.2f to %.2f' % ( chamber_center - chamber_half_width, 
		# 							  chamber_center + chamber_half_width )
		# else:
		# 	print 'Hit in station %d, sector %d, ring %d, chamber %d OK!' % ( Hit.Station(), Hit.Sector(), Hit.Ring(), Hit.Chamber() )
		# return phi_glob_deg - chamber_center
	
def TracksMatch( Trk1, Trk2 ):

	# ## if ( Trk1.First_BX() == Trk2.First_BX() and abs(Trk1.Eta_GMT() - Trk2.Eta_GMT()) < 2 and abs(Trk1.Phi_GMT() - Trk2.Phi_GMT()) < 5 ):
	# if ( abs(Trk1.Eta_GMT() - Trk2.Eta_GMT()) < 5 and abs(Trk1.Phi_GMT() - Trk2.Phi_GMT()) < 5 ):
	# 	return True
	# else:
	# 	return False

	phi_loc_deg_corr = (Trk1.Phi_loc_int() / (0.625 * 60)) * 0.979755
	phi_GMT = math.floor(phi_loc_deg_corr - 35)

	if (Trk1.Phi_GMT() != phi_GMT):
		print 'Trk1 phi_GMT (calc) = %d (%d) from phi_loc %d' % (Trk1.Phi_GMT(), phi_GMT, Trk1.Phi_loc_int())
	
	if ( Trk1.Phi_loc_int() == Trk2.Phi_loc_int() and Trk1.Sector() == Trk2.Sector() and Trk1.Phi_GMT() != Trk2.Phi_GMT() ):
		print 'Trk1 phi_loc (GMT) = %d (%d), Trk2 phi_loc (GMT) = %d (%d)' % ( Trk1.Phi_loc_int() , Trk1.Phi_GMT(), Trk2.Phi_loc_int() , Trk2.Phi_GMT() )
	
	# ## Exact match requirement
	# if Trk1.Eta_GMT() == Trk2.Eta_GMT() and Trk1.Phi_loc_int() == Trk2.Phi_loc_int() and Trk1.BX() == Trk2.BX() and Trk1.Mode() == Trk2.Mode():
	# 	return True
	# else:
	# 	return False
		
	# if (Trk2.Eta_GMT() == -240 or Trk2.Eta_GMT() == 239):

	# if ( abs(Trk1.Eta() - Trk2.Eta()) < 0.05 and CalcDPhi(Trk1.Phi_glob_rad(), Trk2.Phi_glob_rad()) < 0.05 ):
	if ( abs(Trk1.Eta_GMT() - Trk2.Eta_GMT()) < 6 and abs(Trk1.Phi_GMT() - Trk2.Phi_GMT()) < 6 and
	     ( Trk1.Sector() == Trk2.Sector() or Trk1.Sector_GMT() == Trk2.Sector_GMT() or Trk1.Sector_index() == Trk2.Sector_index() ) ):
		return True
		# elif ( Trk1.Sector() == Trk2.Sector() + 1 and abs(Trk1.Phi_GMT() + 95 - Trk2.Phi_GMT()) < 8 ):
		# 	return True
		# elif ( Trk1.Sector() == 1 and Trk2.Sector() == 6 and abs(Trk1.Phi_GMT() + 95 - Trk2.Phi_GMT()) < 8 ):
		# 	return True
	else: return False
	

def PtLutAddrMatch( Trk1, Trk2 ):

	# ## Eta address is still screwed up - AWB 29.04.16
	# if ( Trk1.Pt_LUT_addr() == Trk2.Pt_LUT_addr() ): return True
	# else: return False

	if ( Trk1.DPhi_12() == Trk2.DPhi_12() and Trk1.DPhi_13() == Trk2.DPhi_13() and Trk1.DPhi_14() == Trk2.DPhi_14() and
	     Trk1.DPhi_23() == Trk2.DPhi_23() and Trk1.DPhi_24() == Trk2.DPhi_24() and Trk1.DPhi_34() == Trk2.DPhi_34() and
	     Trk1.DTheta_12() == Trk2.DTheta_12() and Trk1.DTheta_13() == Trk2.DTheta_13() and Trk1.DTheta_14() == Trk2.DTheta_14() and
	     Trk1.DTheta_23() == Trk2.DTheta_23() and Trk1.DTheta_24() == Trk2.DTheta_24() and Trk1.DTheta_34() == Trk2.DTheta_34() and
	     Trk1.CLCT_1() == Trk2.CLCT_1() and Trk1.CLCT_2() == Trk2.CLCT_2() and Trk1.CLCT_3() == Trk2.CLCT_3() and Trk1.CLCT_4() == Trk2.CLCT_4() and
	     True ):
	     # Trk1.FR_1() == Trk2.FR_1() and Trk1.FR_2() == Trk2.FR_2() and Trk1.FR_3() == Trk2.FR_3() and Trk1.FR_4() == Trk2.FR_4() ):
		return True
	else: return False


def PrintEMTFHit( Hit ):
	print 'BX = %d, endcap = %d, sector = %d, subsector = %d, station = %d,' % ( Hit.BX(), Hit.Endcap(), Hit.Sector(), Hit.Subsector(), Hit.Station() ), \
	    'ring = %d, CSC ID = %d, chamber = %d, strip = %d, wire = %d,' % ( Hit.Ring(), Hit.CSC_ID(), Hit.Chamber(), Hit.Strip(), Hit.Wire() ), \
	    'neighbor = %d, bend = %d, CLCT pattern = %d, quality = %d, valid = %d' % ( Hit.Neighbor(), Hit.Bend(), Hit.Pattern(), Hit.Quality(), Hit.Valid() )

def PrintEMTFHitExtra( Hit ):
	PrintEMTFHit( Hit )
	print 'phi_loc_int = %d, theta_int = %d, phi_glob_deg = %.1f, eta = %.3f' % ( Hit.Phi_loc_int(), Hit.Theta_int(), Hit.Phi_glob_deg(), Hit.Eta() )

def PrintEMTFTrack( Trk ):
	print 'BX = %d, endcap = %d, sector = %d, mode = %d, quality = %d, phi_loc_int = %d,' % ( Trk.BX(), Trk.Endcap(), Trk.Sector(), Trk.Mode(), Trk.Quality(), Trk.Phi_loc_int() ), \
	    'phi_GMT = %d, eta_GMT = %d, pT_GMT = %d, phi_glob_deg = %.1f, eta = %.3f, pT = %.1f,' % ( Trk.Phi_GMT(), Trk.Eta_GMT(), Trk.Pt_GMT(), Trk.Phi_glob_deg(), Trk.Eta(), Trk.Pt() ), \
	    'has some (all) neighbor hits = %d (%d)' % ( Trk.Has_neighbor(), Trk.All_neighbor() ) 
	
def PrintSimulatorHitHeader():
	print 'HITS FOR SIMULATOR: tbin, endcap, sector, subsector, station, valid, quality, CLCT pattern, wiregroup, CSC ID, bend angle, halfstrip'

def PrintSimulatorHit( Hit ):
	
	tbin = Hit.BX() + 3
	endcap = 1 if Hit.Endcap() == 1 else 2
	subsector = 0 if Hit.Station() != 1 else Hit.Subsector()
	station = 5 if Hit.Neighbor() == 1 else Hit.Station()
	valid = Hit.Valid()
	if valid != 1: print 'ERROR!!! LCT with Valid = %d' % valid
	if Hit.Neighbor() == 0: CSC_ID = Hit.CSC_ID()
	else:
		if Hit.Station() == 1: CSC_ID = Hit.CSC_ID() / 3
		else: CSC_ID = (2 * Hit.Station()) + ((Hit.CSC_ID() - 3) / 6) 
	bend = 0
	halfstrip = Hit.Strip() + 128 if Hit.Ring() == 4 and Hit.Strip() < 128 else Hit.Strip()

	print '%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d' % ( tbin, endcap, Hit.Sector(), subsector, station, valid,
								 Hit.Quality(), Hit.Pattern(), Hit.Wire(), CSC_ID, bend, halfstrip )

def PrintEventHeaderHeader():
	print 'Event Header output: endcap, sector, sp_ts, tbin, me1a, me1b, me2, me3, me4'
def PrintEventHeader( HD ):
	print '%d, %d, %d, %d, %d, %d, %d, %d, %d' % ( HD.Endcap(), HD.Sector(), HD.SP_TS(), HD.TBIN(), HD.ME1a(), HD.ME1b(), HD.ME2(), HD.ME3(), HD.ME4() )

def PrintMEHeader():
	print 'ME output: tbin, station, vp, quality, clct_pattern, wire, csc_id, lr, strip'
def PrintME( ME ):
	print '%d, %d, %d, %d, %d, %d, %d, %d, %d' % ( ME.TBIN(), ME.Station(), ME.VP(), ME.Quality(), ME.CLCT_pattern(), ME.Wire(), ME.CSC_ID(), ME.LR(), ME.Strip() )

def PrintSPHeader():
	print 'SP output: phi_full, phi_GMT, eta_GMT, pt_GMT, quality_GMT, mode, tbin, me1_subsector, me1_csc_id, me1_delay, me2_csc_id, me2_delay, me3_csc_id, me3_delay, me4_csc_id, me4_delay'
def PrintSP( SP ):
	print '%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d' % ( SP.Phi_full(), SP.Phi_GMT(), SP.Eta_GMT(), SP.Pt_GMT(), SP.Quality_GMT(), SP.Mode(), 
										   SP.TBIN(), SP.ME1_subsector(), SP.ME1_CSC_ID(), SP.ME1_delay(), SP.ME2_CSC_ID(), 
										   SP.ME2_delay(), SP.ME3_CSC_ID(), SP.ME3_delay(), SP.ME4_CSC_ID(), SP.ME4_delay() )

def PrintPtLUT( Trk ):

	if (Trk.DPhi_12() != -999): print('dPhi_12 = %d,' % Trk.DPhi_12()), 
	if (Trk.DPhi_13() != -999): print('dPhi_13 = %d,' % Trk.DPhi_13()), 
	if (Trk.DPhi_14() != -999): print('dPhi_14 = %d,' % Trk.DPhi_14()), 
	if (Trk.DPhi_23() != -999): print('dPhi_23 = %d,' % Trk.DPhi_23()), 
	if (Trk.DPhi_24() != -999): print('dPhi_24 = %d,' % Trk.DPhi_24()), 
	if (Trk.DPhi_34() != -999): print('dPhi_34 = %d,' % Trk.DPhi_34()),
	if (Trk.DTheta_12() != -999): print('dTheta_12 = %d,' % Trk.DTheta_12()), 
	if (Trk.DTheta_13() != -999): print('dTheta_13 = %d,' % Trk.DTheta_13()), 
	if (Trk.DTheta_14() != -999): print('dTheta_14 = %d,' % Trk.DTheta_14()), 
	if (Trk.DTheta_23() != -999): print('dTheta_23 = %d,' % Trk.DTheta_23()), 
	if (Trk.DTheta_24() != -999): print('dTheta_24 = %d,' % Trk.DTheta_24()), 
	if (Trk.DTheta_34() != -999): print('dTheta_34 = %d,' % Trk.DTheta_34()),
	if (Trk.CLCT_1() != -999): print('clct_1 = %d,' % Trk.CLCT_1()),
	if (Trk.CLCT_2() != -999): print('clct_2 = %d,' % Trk.CLCT_2()),
	if (Trk.CLCT_3() != -999): print('clct_3 = %d,' % Trk.CLCT_3()),
	if (Trk.CLCT_4() != -999): print('clct_4 = %d,' % Trk.CLCT_4()),
	if (Trk.FR_1() != -999): print('fr_1 = %d,' % Trk.FR_1()),
	if (Trk.FR_2() != -999): print('fr_2 = %d,' % Trk.FR_2()),
	if (Trk.FR_3() != -999): print('fr_3 = %d,' % Trk.FR_3()),
	if (Trk.FR_4() != -999): print('fr_4 = %d,' % Trk.FR_4()),
	print 'address = %d' % Trk.Pt_LUT_addr()

