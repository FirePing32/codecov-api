ssh_private_key = `cat ~/.ssh/codecov-io_rsa`
sha := $(shell git rev-parse --short=7 HEAD)
release_version = `cat VERSION`
build_date ?= $(shell git show -s --date=iso8601-strict --pretty=format:%cd $$sha)
branch = $(shell git branch | grep \* | cut -f2 -d' ')

build:
	docker build -f Dockerfile . -t codecov/api:latest --build-arg SSH_PRIVATE_KEY="${ssh_private_key}"

build.enterprise:
	docker build -f Dockerfile.enterprise . -t codecov/enterprise-api:${release_version} \
		--label "org.label-schema.build-date"="$(build_date)" \
		--label "org.label-schema.name"="Self-Hosted" \
		--label "org.label-schema.vendor"="Codecov" \
		--label "org.label-schema.version"="${release_version}" \
		--squash



build.enterprise-private:
	docker build -f Dockerfile.enterprise . -t codecov/enterprise-private-api:${release_version}-${sha} \
		--label "org.label-schema.build-date"="$(build_date)" \
		--label "org.label-schema.name"="Self-Hosted API" \
		--label "org.label-schema.vendor"="Codecov" \
		--label "org.label-schema.version"="${release_version}-${sha}" \
		--label "org.vcs-branch"="$(branch)" \
		--squash

check-for-migration-conflicts:
	python manage.py check_for_migration_conflicts

push.enterprise-private:
	docker push codecov/enterprise-private-api:${release_version}-${sha}

push.enterprise:
	docker push codecov/enterprise-api:${release_version}
	docker tag codecov/enterprise-api:${release_version} codecov/enterprise-api:latest-stable
	docker push codecov/enterprise-api:latest-stable

test:
	python -m pytest --cov=./

test.unit:
	python -m pytest --cov=./ -m "not integration" --cov-report=xml:unit.coverage.xml

test.integration:
	python -m pytest --cov=./ -m "integration" --cov-report=xml:integration.coverage.xml
