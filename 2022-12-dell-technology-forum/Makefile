LFS_SHARE_DIR="file://$(PWD)/share"
IPFS_HTTP_GATEWAY=http://localhost:8080/

IPNS_KEY__MATCHES=k51qzi5uqu5di9hgwaga2xcyxnu5cfhfldt1hpmhsq4e9up0vjx5ifo0uenfbn
IPNS_KEY__PLAYER_SCORES=k51qzi5uqu5dkp2iz01edud63wkn7ho00km4i8olenjciz2holb2q6j7b6ervv
IPNS_KEY__PLAYER_SCORES_TOTAL=k51qzi5uqu5dkkzjw4zw4khrnbv7r5wx4tbrlh258zsb2xhhsnzcksqcxsupo1


#########################################################################################
# Ingest
#########################################################################################

init-ingest-lfs:
	@rm -rf share

	@cd ingest && \
		rm -rf .kamu/ replays-staged/ && \
		kamu init && \
		kamu add -r datasets/ && \
		kamu repo add share "$(LFS_SHARE_DIR)" && \
		kamu push matches --to share/matches && \
		kamu push player-scores --to share/player-scores && \
		kamu push player-scores-total --to share/player-scores-total


init-ingest:
	@# Clean up old IPNS keys
	@ipfs key list | grep rl-demo | xargs --no-run-if-empty ipfs key rm > /dev/null

	@# Add dataset IPNS keys
	@cd ingest/keys && \
		ipfs key import rl-demo-matches ipns-matches.key > /dev/null && \
		ipfs key import rl-demo-player-scores ipns-player-scores.key > /dev/null && \
		ipfs key import rl-demo-player-scores-total ipns-player-scores-total.key > /dev/null
	
	@# Init and sync datasets
	@cd ingest && \
		rm -rf .kamu/ replays-staged/ && \
		kamu init && \
		kamu config set protocol.ipfs.httpGateway "$(IPFS_HTTP_GATEWAY)" && \
		kamu add -r datasets/ && \
		kamu push matches --to "ipns://$(IPNS_KEY__MATCHES)" --force && \
		kamu push player-scores --to "ipns://$(IPNS_KEY__PLAYER_SCORES)" --force && \
		kamu push player-scores-total --to "ipns://$(IPNS_KEY__PLAYER_SCORES_TOTAL)" --force


ingest-loop:
	@cd ingest && python -m ingest


#########################################################################################
# Frontend
#########################################################################################

init-frontend-lsf:
	@cd frontend && \
		rm -rf .kamu && \
		kamu init && \
		kamu repo add share "$(LFS_SHARE_DIR)" && \
		kamu pull share/matches && \
		kamu pull share/player-scores && \
		kamu pull share/player-scores-total


init-frontend:
	@cd frontend && \
		rm -rf .kamu && \
		kamu init && \
		kamu config set protocol.ipfs.httpGateway "$(IPFS_HTTP_GATEWAY)" && \
		kamu pull "ipns://$(IPNS_KEY__MATCHES)" --as matches && \
		kamu pull "ipns://$(IPNS_KEY__PLAYER_SCORES)" --as player-scores && \
		kamu pull "ipns://$(IPNS_KEY__PLAYER_SCORES_TOTAL)" --as player-scores-total


#########################################################################################
# Misc
#########################################################################################

clean-kamu:
	rm -rf share
	rm -rf ingest/.kamu
	rm -rf frontend/.kamu


clean-ipfs:
	@# Clean up IPNS keys
	ipfs key list | grep rl-demo | xargs --no-run-if-empty ipfs key rm

	@# Clean up pins
	ipfs pin ls -t recursive -q | xargs --no-run-if-empty ipfs pin rm


clean-replays:
	rm -rf ingest/replays ingest/replays-staged


clean-all: clean-kamu clean-ipfs clean-replays
