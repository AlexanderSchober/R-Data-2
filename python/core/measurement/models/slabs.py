#  -*- coding: utf-8 -*-
# *****************************************************************************
# Copyright (c) 2017 by the NSE analysis contributors (see AUTHORS)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Module authors:
#   Alexander Schober <alex.schober@mac.com>
#
# *****************************************************************************


def slab(meas):

    
    meas.setSample()

    Sample_1 = meas.sample.newElement(
        'Sample_1', 
        volume  = "Cuboid",
        a       = 3.,
        b       = 3.,
        c       = 3.,
        color   = np.asarray([255,0, 0,1]),#colors.map(0.4),
        transp  = 1)
    Sample_1.geometry.buildVolume()
    Sample_1.translate([-1.5,-1.5,3.3])
    Sample_1.rotate([0,0,1], 45)
