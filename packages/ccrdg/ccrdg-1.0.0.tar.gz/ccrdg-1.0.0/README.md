# CerebralCortex-Random-Data-Generator
Generate some random data for Cerebral Cortex Demo Purposes. This script will generate one day worth of sensors data.

### Dependencies
* Python 3.7+
* cerebralcortex-kernel - 3.3.0
    * ```pip3 install cerebralcortex-kernel```

### How to run
* ``python3 main.py``
* By default, random generated data will be stored under home folder, e.g.,``(/Users/ali/cc_data/)``

### How to read generated data
* All the data is stored in parquet files format
* Use CerebralCortex to read the data/metadata
```$xslt
from cerebralcortex.kernel import Kernel

CC = Kernel(cc_configs="default", study_name="mguard")
data = CC.get_stream("battery--org.md2k.phonesensor--phone")
data.show()
```

### Available stream names
* battery--org.md2k.phonesensor--phone
* location--org.md2k.phonesensor--phone
* org.md2k.data_analysis.gps_episodes_and_semantic_location
* accelerometer--org.md2k.phonesensor--phone
* gyroscope--org.md2k.phonesensor--phone
