import pdfmap

def process_block(
    origin,
    page_number,
    x1,
    y1,
    x2,
    y2,
    text,
    confidence
    ):
    if origin is Origin.TOP_LEFT:
        y1, y2 = (round(page_size.height - y2, 2), round(page_size.height - y1, 2))
    elif origin is not Origin.BOTTOM_LEFT:
        raise ValueError(
            f'there is no support for {origin} yet.'
            ' please use either'
            f' {Origin.BOTTOM_LEFT} or {Origin.TOP_LEFT}'
        )

    block = (
        page_number,
        (x1, y1),
        (x2, y2),
        text
        # obj.get_text().replace('\n', '')
    )

    if confidence is not None:
        block += (confidence,)
    
    return block

    # self.word_map.append(block)

def load_pdf(source):
    if isinstance(source, bytes):
        # Use PDF bytes.
        fp = io.BytesIO(source)
    else:
        # Open a PDF file.
        fp = open(source, 'rb')

    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fp)

    # Create a PDF document object that stores the document structure.
    # Password for initialization as 2nd parameter
    document = PDFDocument(parser)

    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()

    # Create a PDF device object.
    device = PDFDevice(rsrcmgr)

    # BEGIN LAYOUT ANALYSIS
    # Set parameters for analysis.
    laparams = LAParams()

    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)

    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
