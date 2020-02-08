// Copyright © 2019 The Things Network Foundation, The Things Industries B.V.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package frequencyplans

import (
	"go.thethings.network/lorawan-stack/pkg/band"
	"go.thethings.network/lorawan-stack/pkg/ttnpb"
)

// CFList generated by this frequency plan, for the version used by a device.
// This function returns nil if the CFList could not be computed, or if the
// device does not support CFLists.
func CFList(fp FrequencyPlan, version ttnpb.PHYVersion) *ttnpb.CFList {
	phy, err := band.GetByID(fp.BandID)
	if err != nil {
		return nil
	}

	phy, err = phy.Version(version)
	if err != nil {
		return nil
	}

	if !phy.ImplementsCFList {
		return nil
	}

	switch phy.CFListType {
	case ttnpb.CFListType_CHANNEL_MASKS:
		return chMaskCFList(fp, phy)
	case ttnpb.CFListType_FREQUENCIES:
		return frequenciesCFList(fp, phy)
	default:
		return nil
	}
}

func chMaskCFList(fp FrequencyPlan, phy band.Band) *ttnpb.CFList {
	cfList := &ttnpb.CFList{
		Type:    ttnpb.CFListType_CHANNEL_MASKS,
		ChMasks: []bool{},
	}

	for _, bandChannel := range phy.UplinkChannels {
		var channelEnabled bool
		for _, fpChannel := range fp.UplinkChannels {
			if fpChannel.Frequency == bandChannel.Frequency {
				channelEnabled = true
			}
		}
		cfList.ChMasks = append(cfList.ChMasks, channelEnabled)
	}

	return cfList
}

func frequenciesCFList(fp FrequencyPlan, phy band.Band) *ttnpb.CFList {
	cfList := &ttnpb.CFList{Type: ttnpb.CFListType_FREQUENCIES}

outer:
	for _, fpChannel := range fp.UplinkChannels {
		for _, bandChannel := range phy.UplinkChannels {
			if fpChannel.Frequency == bandChannel.Frequency {
				continue outer
			}
		}
		cfList.Freq = append(cfList.Freq, uint32(fpChannel.Frequency/phy.FreqMultiplier))
		if len(cfList.Freq) == 5 {
			break
		}
	}

	return cfList
}