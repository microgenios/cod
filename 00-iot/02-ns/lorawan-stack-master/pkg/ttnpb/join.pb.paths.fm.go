// Code generated by protoc-gen-fieldmask. DO NOT EDIT.

package ttnpb

var JoinRequestFieldPathsNested = []string{
	"cf_list",
	"cf_list.ch_masks",
	"cf_list.freq",
	"cf_list.type",
	"correlation_ids",
	"dev_addr",
	"downlink_settings",
	"downlink_settings.opt_neg",
	"downlink_settings.rx1_dr_offset",
	"downlink_settings.rx2_dr",
	"net_id",
	"payload",
	"payload.Payload",
	"payload.Payload.join_accept_payload",
	"payload.Payload.join_accept_payload.cf_list",
	"payload.Payload.join_accept_payload.cf_list.ch_masks",
	"payload.Payload.join_accept_payload.cf_list.freq",
	"payload.Payload.join_accept_payload.cf_list.type",
	"payload.Payload.join_accept_payload.dev_addr",
	"payload.Payload.join_accept_payload.dl_settings",
	"payload.Payload.join_accept_payload.dl_settings.opt_neg",
	"payload.Payload.join_accept_payload.dl_settings.rx1_dr_offset",
	"payload.Payload.join_accept_payload.dl_settings.rx2_dr",
	"payload.Payload.join_accept_payload.encrypted",
	"payload.Payload.join_accept_payload.join_nonce",
	"payload.Payload.join_accept_payload.net_id",
	"payload.Payload.join_accept_payload.rx_delay",
	"payload.Payload.join_request_payload",
	"payload.Payload.join_request_payload.dev_eui",
	"payload.Payload.join_request_payload.dev_nonce",
	"payload.Payload.join_request_payload.join_eui",
	"payload.Payload.mac_payload",
	"payload.Payload.mac_payload.decoded_payload",
	"payload.Payload.mac_payload.f_hdr",
	"payload.Payload.mac_payload.f_hdr.dev_addr",
	"payload.Payload.mac_payload.f_hdr.f_cnt",
	"payload.Payload.mac_payload.f_hdr.f_ctrl",
	"payload.Payload.mac_payload.f_hdr.f_ctrl.ack",
	"payload.Payload.mac_payload.f_hdr.f_ctrl.adr",
	"payload.Payload.mac_payload.f_hdr.f_ctrl.adr_ack_req",
	"payload.Payload.mac_payload.f_hdr.f_ctrl.class_b",
	"payload.Payload.mac_payload.f_hdr.f_ctrl.f_pending",
	"payload.Payload.mac_payload.f_hdr.f_opts",
	"payload.Payload.mac_payload.f_port",
	"payload.Payload.mac_payload.frm_payload",
	"payload.Payload.rejoin_request_payload",
	"payload.Payload.rejoin_request_payload.dev_eui",
	"payload.Payload.rejoin_request_payload.join_eui",
	"payload.Payload.rejoin_request_payload.net_id",
	"payload.Payload.rejoin_request_payload.rejoin_cnt",
	"payload.Payload.rejoin_request_payload.rejoin_type",
	"payload.m_hdr",
	"payload.m_hdr.m_type",
	"payload.m_hdr.major",
	"payload.mic",
	"raw_payload",
	"rx_delay",
	"selected_mac_version",
}

var JoinRequestFieldPathsTopLevel = []string{
	"cf_list",
	"correlation_ids",
	"dev_addr",
	"downlink_settings",
	"net_id",
	"payload",
	"raw_payload",
	"rx_delay",
	"selected_mac_version",
}
var JoinResponseFieldPathsNested = []string{
	"correlation_ids",
	"lifetime",
	"raw_payload",
	"session_keys",
	"session_keys.app_s_key",
	"session_keys.app_s_key.encrypted_key",
	"session_keys.app_s_key.kek_label",
	"session_keys.app_s_key.key",
	"session_keys.f_nwk_s_int_key",
	"session_keys.f_nwk_s_int_key.encrypted_key",
	"session_keys.f_nwk_s_int_key.kek_label",
	"session_keys.f_nwk_s_int_key.key",
	"session_keys.nwk_s_enc_key",
	"session_keys.nwk_s_enc_key.encrypted_key",
	"session_keys.nwk_s_enc_key.kek_label",
	"session_keys.nwk_s_enc_key.key",
	"session_keys.s_nwk_s_int_key",
	"session_keys.s_nwk_s_int_key.encrypted_key",
	"session_keys.s_nwk_s_int_key.kek_label",
	"session_keys.s_nwk_s_int_key.key",
	"session_keys.session_key_id",
}

var JoinResponseFieldPathsTopLevel = []string{
	"correlation_ids",
	"lifetime",
	"raw_payload",
	"session_keys",
}