<?
ob_start();
include 'Classes/PHPExcel.php';
$objReader = PHPExcel_IOFactory::createReader('Excel5');   
$excel = $objReader->load('sheet.xls');
$count = 0;
foreach($_POST as $csv)
{
    $read = 0;  // Read head
    $values = explode(',',$csv);
    $worksheet = $excel->getActiveSheet();
    if ($count != 0)
    {
	$new_worksheet = clone $worksheet;
        //$worksheet1->setTitle('~'.$worksheet->getTitle());
	$excel->addSheet($new_worksheet);
    }
    $excel->setActiveSheetIndex($count);
    
    $worksheet = $excel->getActiveSheet();
    $worksheet->setCellValueByColumnAndRow(6,2,$values[$read]); // year
    $read++;
    $worksheet->setCellValueByColumnAndRow(7,2,$values[$read]); // term
    $read++;
    $worksheet->setCellValueByColumnAndRow(8,2,$values[$read]); // department
    $read++;
    $worksheet->setCellValueByColumnAndRow(9,2,$values[$read]); // code
    $read++;
    $worksheet->setCellValueByColumnAndRow(10,2,$values[$read]); // section
    $read++;
    $worksheet->setCellValueByColumnAndRow(6,4,$values[$read]); // prof
    $read++;
    $worksheet->setCellValueByColumnAndRow(7,5,$values[$read]); // first test
    $read++;
    $worksheet->setCellValueByColumnAndRow(12,5,$values[$read]); // total sess
    $read++;
    $worksheet->setCellValueByColumnAndRow(9,4,$values[$read]); // leader name
    $read++;

    $end = count($values);
    $row = 8;
    while($read < $end) // iterate through students
    {
	for ($i=6;$i<14;$i++)
	{
	    if ($i==9){
		if ($values[$read] == 'False')
		    $values[$read] = 'No';
		else
		    $values[$read] = 'Yes';
	    }
	    $worksheet->setCellValueByColumnAndRow($i,$row,$values[$read]);
	    $read++;
	}
	$row++;
    }
    $count++;
}

$objWriter = PHPExcel_IOFactory::createWriter($excel, 'Excel5');
header('Content-Type: application/vnd.ms-excel');
header('Content-Disposition: attachment;filename="report.xls"');
header('Cache-Control: max-age=0');
// Cleanup
$objWriter->save('php://output');
?>
