## 安装

> pip install ncbi_api
>
> 或者
>
> pip install ncbi_api -i https://pypi.python.org/simple

## 使用

### Geo数据下载

#### Accession列表

- example

  ```python
  from ncbi_api.geo import AccessionDownloader
  
  downloader = AccessionDownloader()
  downloader.start(page_nums=299, display=500)
  ```

#### series_matrix

- example1

  ```python
  from ncbi_api.geo import GeoDownloader, GeoDataType
  
  accessions = ['GSE113138', 'GSE171935', 'GSE164612', 'GSE166066']
  
  geo = GeoDownloader(accession_list=accessions)
  geo.run(data_type=GeoDataType.SeriesMatrix, workers=4)
  ```
  
- 运行

  ```
  -*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-
  正在读取 Accession 列表
  	--> 共有 Accession 数量：4
  -*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-
  成功读取并完成过滤 -> takes 0.104 seconds
  https://ftp.ncbi.nlm.nih.gov/geo/series/GSE166nnn/GSE166066/matrix/
  https://ftp.ncbi.nlm.nih.gov/geo/series/GSE171nnn/GSE171935/matrix/
  https://ftp.ncbi.nlm.nih.gov/geo/series/GSE113nnn/GSE113138/matrix/
  https://ftp.ncbi.nlm.nih.gov/geo/series/GSE164nnn/GSE164612/matrix/
  GSE113138 200
  GSE164612 200
  GSE171935 200
  GSE166066 200
  -*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-
  正在读取 Accession 列表
  	--> 共有 Accession 数量：4, 成功下载：4, 下载失败(404)：0,  还剩：0
  -*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-
  成功读取并完成过滤 -> takes 0.046 seconds
  -*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-
  正在读取 url 列表
  	--> 共有 url 数量：4
  -*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-
  成功读取并完成过滤 -> takes 0.004 seconds
  正在下载 -> GSE113138_series_matrix.txt.gz -> 3.18 KB: 4KB [00:00, 1999.91KB/s]                   
  正在下载 -> GSE166066_series_matrix.txt.gz -> 3.01 KB: 4KB [00:00, 1333.64KB/s]                   
  正在下载 -> GSE164612_series_matrix.txt.gz -> 2.21 MB:  21%|█    | 465/2258 [00:31<02:02, 14.60KB/s]
  ```
  
- example2

  ```python
  from ncbi_api.geo import GeoDownloader, GeoDataType
  
  accessions = ['GSE113138', 'GSE171935', 'GSE164612', 'GSE166066']
  
  geo = GeoDownloader(accession_list=accessions)
  geo.run(data_type=GeoDataType.SeriesMatrix, workers=4, series_matrix_url_filepath='history/series_matrix_urls.txt')
  ```
  
- 运行

  ```
  -*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-
  正在读取 url 列表
  	--> 共有 url 数量：4, 成功下载：3, 下载失败(404)：0,  还剩：1
  -*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-
  成功读取并完成过滤 -> takes 0.002 seconds
  
  正在下载 -> GSE171935_series_matrix.txt.gz -> 1.86 KB: 2KB [00:00, 666.93KB/s]                     
  正在下载 -> GSE113138_series_matrix.txt.gz -> 3.18 KB: 4KB [00:00, 1335.45KB/s]                   
  正在下载 -> GSE166066_series_matrix.txt.gz -> 3.02 KB: 4KB [00:00, 14.50KB/s]                     
  正在下载 -> GSE164612_series_matrix.txt.gz -> 2.21 MB:  49%|█▉  | 1105/2258 [00:46<00:28, 41.07KB/s]
  ```

### Geo数据解压缩

- example

  ```python
  from zyf.file import scan_directory_contents
  
  from ncbi_api.compress import Gzip
  
  file_list = scan_directory_contents('download')
  
  gzip = Gzip()
  gzip.batch_file_unzip(file_list, unzip_dir='unzip')
  ```

### Geo数据解析

- example

  ```python
  from zyf.file import scan_directory_contents
  
  from ncbi_api.geo import GeoParser, GeoDataType
  
  file_list = scan_directory_contents('unzip')
  parser = GeoParser(file_list=file_list)
  parser.run(GeoDataType.SeriesMatrix, workers=8)
  ```

  