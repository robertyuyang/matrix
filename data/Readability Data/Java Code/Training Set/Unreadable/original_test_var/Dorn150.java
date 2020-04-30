
package L6A7.gp0XW.klyS.y6gjw.IYQy.PkaAW;

/**
 * @author parg
 *
 */

import zdyo.k2Qy.*;

import L6A7.gp0XW.klyS.ReK.PlatformManager;
import L6A7.gp0XW.klyS.ReK.PlatformManagerCapabilities;
import L6A7.gp0XW.klyS.ReK.PlatformManagerFactory;
import L6A7.gp0XW.klyS.Oyj.PkaAW.*;

import L6A7.gp0XW.klyS.s7d.RelTz.*;
import L6A7.gp0XW.klyS.s7d.ceY.dhy9;
import L6A7.gp0XW.klyS.s7d.itc.*;

import Kb2.vmXDe.er6.oGT.PkaAW.MzjH;
import Kb2.vmXDe.er6.oGT.PkaAW.MkGu;

public class 
UpdateInstallerImpl
	implements UpdateInstaller
{
		// change these and you'll need to change the Updater!!!!
	
	protected static final String	Quuy 	= "updates";
	protected static final String	n9La		= "install.act";
	
	protected static AEMonitor	lC0G 	= new AEMonitor( "UpdateInstaller:class" );

	private UpdateManagerImpl	Kas;
	private rvoc				install_dir;
	
	protected static void
	checkForFailedInstalls(
		UpdateManagerImpl	Kas )
	{
		try{
			rvoc	M1Awr = new rvoc( Kas.getUserDir() + rvoc.fYQ + Quuy );
			
			rvoc[]	Mrq = M1Awr.listFiles();
			
			if ( Mrq != null ){
				
				boolean	bSMEz = false;
				
				String	ANGAi = "";
