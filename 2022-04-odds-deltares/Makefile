IPFS_HTTP_GATEWAY=http://localhost:8080/

IPNS_KEY__BOVEN_RIJN=k51qzi5uqu5dhyb8gvuym6s0ylbttwlw1l1yjfhy3t562lhdx9rp8wvs05vj29
IPNS_KEY__IJSSEL=k51qzi5uqu5dkej6mns4v5sjvllh9bx0pzjd14wf95ud3xr5hzfmay9gftu4wj
IPNS_KEY__LEK=k51qzi5uqu5dmezf42vs30ucbhos2jqqdpli74nykgk9lreqdo2ulx0eyi3nms
IPNS_KEY__NEDERRIJN=k51qzi5uqu5dilaqi4l7dpgyeo9hulrk6p0hi42dqvt1ivxcch8a6ajuvtzt1s
IPNS_KEY__PANNERDENSCH_KANAAL=k51qzi5uqu5dhiw9ppjw6hlkg1kxg18cmcastm4v9r96cjntpgcjxsjk6bkqtt
IPNS_KEY__WAAL=k51qzi5uqu5djkitjfhb2ndz8s76ypz0ujzd4lh8gwcxdmxy5za54skovyp4us

IPNS_KEY__STATIONS=k51qzi5uqu5dgp94s1dzxjmkc3yxyol4s8gvgtvsm1vjqhqzv8n1slhl9vxzh7
IPNS_KEY__RHINE_NL=k51qzi5uqu5dlupxrihl3uz6oxtr53qz1c9hp2m3b36t7fej4zbei6hbk3d76c
IPNS_KEY__RHINE_NL_SIM=k51qzi5uqu5di6fm2mbgkukilpwvrpe5idqlyunspfk37campf4woptqxvacy1


.PHONY: data-raw
data-raw:
	aws s3 cp --recursive "s3://backups.kamu.dev/demos/2022-04-odds-deltares/data/" data/raw/

.PHONY: data-prepared
data-prepared:
	aws s3 cp --recursive "s3://backups.kamu.dev/demos/2022-04-odds-deltares/data-prepared/" data/prep/


.PHONY: workspace
workspace:
	kamu init --multi-tenant
	cp utils/.kamuconfig .kamu/
	
	kamu --account rijkswaterstaat.nl add datasets/measurements.*
	kamu --account rijkswaterstaat.nl add datasets/stations.*
	kamu --account rijkswaterstaat.nl pull --all
	
	kamu --account deltares.nl add datasets/rhine-basin.*
	kamu --account deltares.nl pull rhine-basin.netherlands
	kamu --account deltares.nl pull rhine-basin.netherlands.sim-data
	kamu --account deltares.nl pull rhine-basin.netherlands.sim


.PHONY: init-s3-root
init-s3-root:
	kamu init
	@# kamu pull "ipns://stations.waterinfo.rws.nl.opendatafabric.net" --as stations
	kamu pull "https://s3.us-west-2.amazonaws.com/datasets.kamu.dev/demo/deltares/stations"
	kamu pull "https://s3.us-west-2.amazonaws.com/datasets.kamu.dev/demo/deltares/measurements.boven-rijn"
	kamu pull "https://s3.us-west-2.amazonaws.com/datasets.kamu.dev/demo/deltares/measurements.ijssel"
	kamu pull "https://s3.us-west-2.amazonaws.com/datasets.kamu.dev/demo/deltares/measurements.lek"
	kamu pull "https://s3.us-west-2.amazonaws.com/datasets.kamu.dev/demo/deltares/measurements.nederrijn"
	kamu pull "https://s3.us-west-2.amazonaws.com/datasets.kamu.dev/demo/deltares/measurements.pannerdensch-kanaal"
	kamu pull "https://s3.us-west-2.amazonaws.com/datasets.kamu.dev/demo/deltares/measurements.waal"


.PHONY: init-s3
init-s3: init-s3-root
	kamu pull "https://s3.us-west-2.amazonaws.com/datasets.kamu.dev/demo/deltares/rhine-basin.netherlands"
	kamu pull "https://s3.us-west-2.amazonaws.com/datasets.kamu.dev/demo/deltares/rhine-basin.netherlands.sim"


.PHONY: push-s3
push-s3:
	kamu push measurements.boven-rijn --to "s3://datasets.kamu.dev/demo/deltares/measurements.boven-rijn"
	kamu push measurements.ijssel --to "s3://datasets.kamu.dev/demo/deltares/measurements.ijssel"
	kamu push measurements.lek --to "s3://datasets.kamu.dev/demo/deltares/measurements.lek"
	kamu push measurements.nederrijn --to "s3://datasets.kamu.dev/demo/deltares/measurements.nederrijn"
	kamu push measurements.pannerdensch-kanaal --to "s3://datasets.kamu.dev/demo/deltares/measurements.pannerdensch-kanaal"
	kamu push measurements.waal --to "s3://datasets.kamu.dev/demo/deltares/measurements.waal"
	kamu push rhine-basin.netherlands --to "s3://datasets.kamu.dev/demo/deltares/rhine-basin.netherlands"
	kamu push rhine-basin.netherlands.sim --to "s3://datasets.kamu.dev/demo/deltares/rhine-basin.netherlands.sim"
	kamu push stations --to "s3://datasets.kamu.dev/demo/deltares/stations"


.PHONY: push-s3-rm
push-s3-rm:
	aws s3 rm --recursive "s3://datasets.kamu.dev/demo/deltares"


.PHONY: ipns-keys
ipns-keys: clean-ipns-keys
	@# Add dataset IPNS keys
	@cd keys/ && \
		ipfs key import demo-deltares-boven-rijn boven-rijn.key > /dev/null  && \
		ipfs key import demo-deltares-ijssel ijssel.key > /dev/null  && \
		ipfs key import demo-deltares-lek lek.key > /dev/null  && \
		ipfs key import demo-deltares-nederrijn nederrijn.key > /dev/null  && \
		ipfs key import demo-deltares-pannerdensch-kanaal pannerdensch-kanaal.key > /dev/null  && \
		ipfs key import demo-deltares-waal waal.key > /dev/null  && \
		ipfs key import demo-deltares-stations stations.key > /dev/null  && \
		ipfs key import demo-deltares-rhine-basin.netherlands rhine-basin.netherlands.key > /dev/null  && \
		ipfs key import demo-deltares-rhine-basin.netherlands.sim rhine-basin.netherlands.sim.key > /dev/null


.PHONY: clean-ipns-keys
clean-ipns-keys:
	@# Clean up old IPNS keys
	@ipfs key list | grep demo-deltares- | xargs --no-run-if-empty ipfs key rm > /dev/null


.PHONY: push-ipns
push-ipns:
	kamu push measurements.boven-rijn --to "ipns://$(IPNS_KEY__BOVEN_RIJN)"
	kamu push measurements.ijssel --to "ipns://$(IPNS_KEY__IJSSEL)"
	kamu push measurements.lek --to "ipns://$(IPNS_KEY__LEK)"
	kamu push measurements.nederrijn --to "ipns://$(IPNS_KEY__NEDERRIJN)"
	kamu push measurements.pannerdensch-kanaal --to "ipns://$(IPNS_KEY__PANNERDENSCH_KANAAL)"
	kamu push measurements.waal --to "ipns://$(IPNS_KEY__WAAL)"
	kamu push stations --to "ipns://$(IPNS_KEY__STATIONS)"
	kamu push rhine-basin.netherlands --to "ipns://$(IPNS_KEY__RHINE_NL)"
	kamu push rhine-basin.netherlands.sim --to "ipns://$(IPNS_KEY__RHINE_NL_SIM)"


.PHONY: init-ipfs
init-ipfs:
	kamu init
	kamu config set protocol.ipfs.httpGateway "$(IPFS_HTTP_GATEWAY)"
	kamu pull "ipns://$(IPNS_KEY__BOVEN_RIJN)" --as measurements.boven-rijn
	kamu pull "ipns://$(IPNS_KEY__IJSSEL)" --as measurements.ijssel
	kamu pull "ipns://$(IPNS_KEY__LEK)" --as measurements.lek
	kamu pull "ipns://$(IPNS_KEY__NEDERRIJN)" --as measurements.nederrijn
	kamu pull "ipns://$(IPNS_KEY__PANNERDENSCH_KANAAL)" --as measurements.pannerdensch-kanaal
	kamu pull "ipns://$(IPNS_KEY__WAAL)" --as measurements.waal
	kamu pull "ipns://$(IPNS_KEY__STATIONS)" --as stations
	kamu pull "ipns://$(IPNS_KEY__RHINE_NL)" --as rhine-basin.netherlands
	kamu pull "ipns://$(IPNS_KEY__RHINE_NL_SIM)" --as rhine-basin.netherlands.sim
